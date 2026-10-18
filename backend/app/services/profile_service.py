import os
from app.extensions import db
from app.models.profile import PatientProfile
from app.models.user import User
from app.utils.errors import NotFoundError, ValidationError
from app.utils.file_handling import save_secure_file
from app.utils.validation import parse_date_safe


class ProfileService:
    @staticmethod
    def get_or_create_profile(user_id: str) -> PatientProfile:
        profile = PatientProfile.query.filter_by(user_id=user_id).first()
        if not profile:
            user = db.session.get(User, user_id)
            if not user:
                raise NotFoundError("User not found.")
            profile = PatientProfile(user_id=user.id, full_name=user.full_name)
            db.session.add(profile)
            profile.calculate_completion()
            db.session.commit()
        return profile

    @staticmethod
    def update_profile(user_id: str, data: dict, partial: bool = True) -> PatientProfile:
        profile = ProfileService.get_or_create_profile(user_id)

        # Mapping direct fields
        direct_fields = [
            "full_name",
            "gender",
            "phone_number",
            "contact_email",
            "address",
            "city",
            "state",
            "blood_group",
            "height_cm",
            "weight_kg",
            "known_allergies",
            "existing_medical_conditions",
            "current_medications",
            "previous_surgeries",
            "family_history_heart_disease",
            "preferred_hospital",
            "preferred_doctor",
            "patient_identifier",
        ]

        for field in direct_fields:
            if field in data:
                setattr(profile, field, data[field])
            elif not partial:
                setattr(profile, field, None)

        # Date of birth parsing
        if "date_of_birth" in data:
            dob_val = data["date_of_birth"]
            if isinstance(dob_val, str):
                parsed = parse_date_safe(dob_val)
                if not parsed and dob_val.strip():
                    raise ValidationError("Invalid date_of_birth format. Expected YYYY-MM-DD.")
                profile.date_of_birth = parsed.date() if parsed else None
            else:
                profile.date_of_birth = dob_val

        # Nested Emergency Contact
        if "emergency_contact" in data and isinstance(data["emergency_contact"], dict):
            em = data["emergency_contact"]
            if "name" in em:
                profile.emergency_contact_name = em["name"]
            if "phone" in em:
                profile.emergency_contact_phone = em["phone"]
            if "relation" in em:
                profile.emergency_contact_relation = em["relation"]

        # Nested Insurance
        if "insurance" in data and isinstance(data["insurance"], dict):
            ins = data["insurance"]
            if "provider" in ins:
                profile.insurance_provider = ins["provider"]
            if "policy_number" in ins:
                profile.insurance_policy_number = ins["policy_number"]

        profile.calculate_completion()
        db.session.commit()
        return profile

    @staticmethod
    def delete_profile(user_id: str):
        profile = PatientProfile.query.filter_by(user_id=user_id).first()
        if not profile:
            raise NotFoundError("Profile not found.")

        # Reset profile fields without deleting user account
        profile.full_name = None
        profile.date_of_birth = None
        profile.gender = None
        profile.phone_number = None
        profile.contact_email = None
        profile.address = None
        profile.city = None
        profile.state = None
        profile.emergency_contact_name = None
        profile.emergency_contact_phone = None
        profile.emergency_contact_relation = None
        profile.blood_group = None
        profile.height_cm = None
        profile.weight_kg = None
        profile.known_allergies = None
        profile.existing_medical_conditions = None
        profile.current_medications = None
        profile.previous_surgeries = None
        profile.family_history_heart_disease = False
        profile.preferred_hospital = None
        profile.preferred_doctor = None
        profile.insurance_provider = None
        profile.insurance_policy_number = None
        profile.patient_identifier = None
        profile.photo_filename = None
        profile.completion_percentage = 0
        db.session.commit()

    @staticmethod
    def upload_photo(user_id: str, file_storage, upload_folder: str, max_bytes: int) -> str:
        profile = ProfileService.get_or_create_profile(user_id)
        photo_dir = os.path.join(upload_folder, "profiles")
        saved_name, _, _ = save_secure_file(
            file_storage,
            target_dir=photo_dir,
            allowed_extensions={"jpg", "jpeg", "png", "webp"},
            max_bytes=max_bytes,
        )

        # Remove old photo if exists
        if profile.photo_filename:
            old_path = os.path.join(photo_dir, profile.photo_filename)
            if os.path.exists(old_path):
                try:
                    os.remove(old_path)
                except OSError:
                    pass

        profile.photo_filename = saved_name
        db.session.commit()
        return saved_name

    @staticmethod
    def get_completion_details(user_id: str) -> dict:
        profile = ProfileService.get_or_create_profile(user_id)
        pct = profile.calculate_completion()
        missing = []
        if not (profile.full_name and profile.date_of_birth):
            missing.append("Basic Information (Full name & DOB)")
        if not profile.gender:
            missing.append("Gender")
        if not (profile.phone_number or profile.contact_email):
            missing.append("Contact Information")
        if not (profile.emergency_contact_name and profile.emergency_contact_phone):
            missing.append("Emergency Contact")
        if not profile.blood_group:
            missing.append("Blood Group")
        if not (profile.height_cm and profile.weight_kg):
            missing.append("Vitals (Height & Weight)")
        if not (profile.existing_medical_conditions or profile.known_allergies):
            missing.append("Clinical History & Known Allergies")

        return {
            "completion_percentage": pct,
            "is_complete": pct >= 90,
            "missing_sections": missing,
        }
