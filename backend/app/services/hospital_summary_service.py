import html
from datetime import datetime, timezone
from app.extensions import db
from app.models.hospital_summary import ConsentRecord, HospitalSummaryPreference
from app.models.lifestyle import LifestyleAssessment
from app.models.prediction import HeartPrediction
from app.models.profile import PatientProfile
from app.models.user import User
from app.utils.errors import BadRequestError, NotFoundError, ValidationError
from app.utils.i18n import get_text


class HospitalSummaryService:
    @staticmethod
    def get_or_create_preferences(user_id: str) -> HospitalSummaryPreference:
        pref = HospitalSummaryPreference.query.filter_by(user_id=user_id).first()
        if not pref:
            pref = HospitalSummaryPreference(user_id=user_id)
            db.session.add(pref)
            db.session.commit()
        return pref

    @staticmethod
    def update_preferences(user_id: str, data: dict) -> HospitalSummaryPreference:
        pref = HospitalSummaryService.get_or_create_preferences(user_id)
        for k, v in data.items():
            if hasattr(pref, k):
                setattr(pref, k, v)
        db.session.commit()
        return pref

    @staticmethod
    def get_summary_data(user_id: str, lang: str = "en") -> dict:
        user = db.session.get(User, user_id)
        if not user:
            raise NotFoundError("User not found.")

        profile = PatientProfile.query.filter_by(user_id=user_id).first()
        pref = HospitalSummaryService.get_or_create_preferences(user_id)

        # Authorized heart assessments
        heart_records = []
        if pref.include_heart_predictions:
            query = (
                HeartPrediction.query.filter_by(user_id=user_id, include_in_hospital_summary=True)
                .order_by(HeartPrediction.created_at.desc())
                .limit(pref.max_heart_records)
            )
            heart_records = [p.to_dict() for p in query.all()]

        # Authorized lifestyle assessments
        lifestyle_records = []
        if pref.include_lifestyle_assessments:
            query = (
                LifestyleAssessment.query.filter_by(user_id=user_id, include_in_hospital_summary=True)
                .order_by(LifestyleAssessment.created_at.desc())
                .limit(pref.max_lifestyle_records)
            )
            lifestyle_records = [l.to_dict() for l in query.all()]

        profile_dict = profile.to_dict() if profile else {}

        return {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "patient_name": profile.full_name if profile and profile.full_name else user.full_name or "Patient",
            "patient_identifier": profile.patient_identifier if profile else None,
            "profile": profile_dict if pref.include_profile else {},
            "vitals": {
                "blood_group": profile.blood_group if profile else None,
                "height_cm": profile.height_cm if profile else None,
                "weight_kg": profile.weight_kg if profile else None,
            },
            "emergency_contact": (
                profile_dict.get("emergency_contact") if pref.include_emergency_contact and profile else None
            ),
            "clinical_background": {
                "allergies": profile.known_allergies if pref.include_allergies and profile else None,
                "existing_conditions": profile.existing_medical_conditions if profile else None,
                "medications": profile.current_medications if pref.include_medications and profile else None,
                "surgeries": profile.previous_surgeries if pref.include_surgeries and profile else None,
                "family_history": profile.family_history_heart_disease if pref.include_family_history and profile else None,
            },
            "heart_predictions": heart_records,
            "lifestyle_assessments": lifestyle_records,
            "disclaimer": get_text("disclaimer", lang),
            "hospital_notice": get_text("hospital_share_notice", lang),
        }

    @staticmethod
    def generate_html_summary(user_id: str, lang: str = "en") -> str:
        data = HospitalSummaryService.get_summary_data(user_id, lang=lang)

        patient_name = html.escape(str(data["patient_name"]))
        patient_id = html.escape(str(data["patient_identifier"] or "N/A"))
        disclaimer = html.escape(str(data["disclaimer"]))
        notice = html.escape(str(data["hospital_notice"]))

        heart_rows = ""
        for h in data["heart_predictions"]:
            prob_str = f"{h['probability']:.1%}" if h.get("probability") is not None else "N/A"
            heart_rows += f"""
            <tr>
                <td>{html.escape(h.get('created_at', '')[:10])}</td>
                <td>{html.escape(h.get('model', ''))}</td>
                <td><strong>{html.escape(h['prediction'].get('label', ''))}</strong></td>
                <td>{prob_str}</td>
            </tr>
            """

        lifestyle_rows = ""
        for l in data["lifestyle_assessments"]:
            lifestyle_rows += f"""
            <tr>
                <td>{html.escape(l.get('created_at', '')[:10])}</td>
                <td><strong>{html.escape(l.get('category_label', ''))}</strong></td>
                <td>{l.get('score', 0)} / 100</td>
            </tr>
            """

        allergies = html.escape(str(data["clinical_background"].get("allergies") or "None reported"))
        meds = html.escape(str(data["clinical_background"].get("medications") or "None reported"))
        conditions = html.escape(str(data["clinical_background"].get("existing_conditions") or "None reported"))
        surgeries = html.escape(str(data["clinical_background"].get("surgeries") or "None reported"))
        blood_group = html.escape(str(data["vitals"].get("blood_group") or "Not recorded"))

        return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
    <meta charset="UTF-8">
    <title>HeartPredict AI - Clinical Summary - {patient_name}</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; line-height: 1.5; color: #1e293b; margin: 40px; }}
        .header {{ border-bottom: 3px solid #0284c7; padding-bottom: 12px; margin-bottom: 24px; }}
        .header h1 {{ margin: 0; color: #0f172a; font-size: 24px; }}
        .header p {{ margin: 4px 0 0 0; color: #64748b; font-size: 14px; }}
        .badge {{ display: inline-block; padding: 3px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; background: #e0f2fe; color: #0369a1; }}
        .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 24px; }}
        .card {{ background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 16px; }}
        .card h3 {{ margin-top: 0; font-size: 16px; color: #334155; border-bottom: 1px solid #cbd5e1; padding-bottom: 6px; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 14px; }}
        th, td {{ padding: 8px 12px; text-align: left; border-bottom: 1px solid #e2e8f0; }}
        th {{ background: #f1f5f9; color: #475569; }}
        .disclaimer {{ background: #fffbeb; border: 1px solid #fef3c7; border-left: 4px solid #f59e0b; padding: 12px; margin-top: 30px; font-size: 13px; color: #92400e; border-radius: 4px; }}
        .actions {{ margin-top: 20px; text-align: right; }}
        @media print {{
            .no-print {{ display: none; }}
            body {{ margin: 20px; }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <span class="badge">HeartPredict AI Clinical Assessment Summary</span>
        <h1>{patient_name}</h1>
        <p>Patient Identifier: <strong>{patient_id}</strong> | Generated on: {data['generated_at'][:10]}</p>
    </div>

    <div class="grid">
        <div class="card">
            <h3>Patient Information & Vitals</h3>
            <p><strong>Blood Group:</strong> {blood_group}</p>
            <p><strong>Height:</strong> {data['vitals'].get('height_cm') or 'N/A'} cm</p>
            <p><strong>Weight:</strong> {data['vitals'].get('weight_kg') or 'N/A'} kg</p>
        </div>
        <div class="card">
            <h3>Medical Background</h3>
            <p><strong>Existing Conditions:</strong> {conditions}</p>
            <p><strong>Known Allergies:</strong> {allergies}</p>
            <p><strong>Current Medications:</strong> {meds}</p>
            <p><strong>Previous Surgeries:</strong> {surgeries}</p>
        </div>
    </div>

    <div class="card" style="margin-bottom: 24px;">
        <h3>Heart Disease Model Predictions (Authorized)</h3>
        <table>
            <thead>
                <tr>
                    <th>Date</th>
                    <th>Model</th>
                    <th>Prediction</th>
                    <th>Probability</th>
                </tr>
            </thead>
            <tbody>
                {heart_rows or '<tr><td colspan="4" style="text-align:center;color:#94a3b8;">No heart predictions authorized for inclusion.</td></tr>'}
            </tbody>
        </table>
    </div>

    <div class="card">
        <h3>Lifestyle Risk Assessments (Authorized)</h3>
        <table>
            <thead>
                <tr>
                    <th>Date</th>
                    <th>Category</th>
                    <th>Score</th>
                </tr>
            </thead>
            <tbody>
                {lifestyle_rows or '<tr><td colspan="3" style="text-align:center;color:#94a3b8;">No lifestyle assessments authorized for inclusion.</td></tr>'}
            </tbody>
        </table>
    </div>

    <div class="disclaimer">
        <strong>Notice:</strong> {notice}<br>
        <strong>Clinical Disclaimer:</strong> {disclaimer}
    </div>

    <div class="actions no-print">
        <button onclick="window.print()" style="padding: 8px 16px; background: #0284c7; color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 14px;">Print / Save as PDF</button>
    </div>
</body>
</html>"""

    @staticmethod
    def share_summary(user_id: str, data: dict, ip_address: str = None, user_agent: str = None) -> dict:
        consent = data.get("consent")
        if not consent:
            raise ValidationError("Explicit consent is required to prepare a shareable summary.")

        consent_text = (
            "User provided explicit consent to prepare and export a clinical discussion summary "
            f"for purpose: '{data.get('purpose', 'General clinical reference')}'."
        )

        record = ConsentRecord(
            user_id=user_id,
            action="share_summary",
            consent_given=True,
            consent_text=consent_text,
            ip_address=ip_address,
            user_agent=user_agent,
        )
        db.session.add(record)
        db.session.commit()

        return {
            "status": "prepared",
            "consent_id": record.id,
            "message": "Clinical summary prepared. No external third-party transmission took place.",
            "recipient_email": data.get("recipient_email"),
            "audit_timestamp": record.created_at.isoformat(),
        }
