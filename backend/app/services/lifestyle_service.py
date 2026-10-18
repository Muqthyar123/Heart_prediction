import json
from datetime import datetime, timezone
from app.extensions import db
from app.models.lifestyle import LifestyleAssessment
from app.utils.errors import ForbiddenError, NotFoundError, ValidationError
from app.utils.i18n import get_text

# Weights for the 7 lifestyle domains (sum to 1.0)
DOMAIN_WEIGHTS = {
    "smoking": 0.22,
    "activity": 0.18,
    "diet": 0.18,
    "stress": 0.14,
    "sleep": 0.10,
    "weight": 0.10,
    "alcohol": 0.08,
}

# Risk points per answer choice: 1 (highest risk) to 4 (lowest risk)
CHOICE_RISK_SCORES = {
    1: 100.0,
    2: 65.0,
    3: 30.0,
    4: 0.0,
}

DOMAIN_LABELS = {
    "activity": "Physical Activity",
    "diet": "Diet & Nutrition",
    "smoking": "Smoking & Tobacco",
    "alcohol": "Alcohol Consumption",
    "sleep": "Sleep Quality & Duration",
    "stress": "Stress Management",
    "weight": "Body Weight & BMI",
}

DOMAIN_RECOMMENDATION_KEYS = {
    "activity": "rec_activity",
    "diet": "rec_diet",
    "smoking": "rec_smoking",
    "alcohol": "rec_alcohol",
    "sleep": "rec_sleep",
    "stress": "rec_stress",
    "weight": "rec_weight",
}


class LifestyleService:
    @staticmethod
    def calculate_assessment(answers: dict, lang: str = "en") -> dict:
        breakdown = []
        weighted_total = 0.0

        for domain, weight in DOMAIN_WEIGHTS.items():
            choice = answers.get(domain)
            if choice not in (1, 2, 3, 4):
                raise ValidationError(f"Invalid answer for '{domain}'. Must be an integer between 1 and 4.")

            domain_score = CHOICE_RISK_SCORES[choice]
            weighted_total += domain_score * weight

            breakdown.append({
                "key": domain,
                "label": DOMAIN_LABELS[domain],
                "score": round(domain_score, 1),
                "weight": weight,
            })

        overall_score = round(weighted_total, 1)

        # Categorization
        if overall_score <= 32.0:
            category = "lower"
            code = "LOWER_RISK"
            label = get_text("lower_risk_label", lang)
        elif overall_score <= 62.0:
            category = "moderate"
            code = "MODERATE_RISK"
            label = get_text("moderate_risk_label", lang)
        else:
            category = "higher"
            code = "HIGHER_RISK"
            label = get_text("higher_risk_label", lang)

        # Build recommendations based on domains that had risk > 30
        recommendations = []
        for item in sorted(breakdown, key=lambda x: x["score"], reverse=True):
            if item["score"] >= 30.0:
                rec_key = DOMAIN_RECOMMENDATION_KEYS.get(item["key"])
                if rec_key:
                    recommendations.append(get_text(rec_key, lang))

        if not recommendations:
            recommendations.append("Continue maintaining your balanced, heart-healthy lifestyle habits!")

        scoring_explanation = (
            f"The lifestyle risk score ({overall_score}/100) is a weighted calculation across 7 key lifestyle domains: "
            "Tobacco exposure (22%), Physical activity (18%), Diet (18%), Stress (14%), Sleep (10%), Weight (10%), and Alcohol (8%). "
            "Lower scores reflect heart-protective habits, while higher scores indicate lifestyle areas that could benefit from improvement."
        )

        return {
            "score": overall_score,
            "category": category,
            "category_label": label,
            "category_code": code,
            "breakdown": breakdown,
            "recommendations": recommendations,
            "scoring_explanation": scoring_explanation,
            "disclaimer": get_text("lifestyle_disclaimer", lang),
        }

    @staticmethod
    def create_assessment(answers: dict, user_id: str = None, save_to_history: bool = True, lang: str = "en") -> dict:
        result = LifestyleService.calculate_assessment(answers, lang=lang)

        record = None
        if user_id and save_to_history:
            record = LifestyleAssessment(
                user_id=user_id,
                answers_json=json.dumps(answers),
                score=result["score"],
                category=result["category"],
                category_label=result["category_label"],
                category_code=result["category_code"],
                breakdown_json=json.dumps(result["breakdown"]),
                recommendations_json=json.dumps(result["recommendations"]),
            )
            db.session.add(record)
            db.session.commit()

        assessment_id = record.id if record else "ephemeral-lifestyle"

        return {
            "assessment_id": assessment_id,
            "user_id": user_id,
            "score": result["score"],
            "category": result["category"],
            "category_label": result["category_label"],
            "category_code": result["category_code"],
            "breakdown": result["breakdown"],
            "recommendations": result["recommendations"],
            "scoring_explanation": result["scoring_explanation"],
            "disclaimer": result["disclaimer"],
            "created_at": record.created_at.isoformat() if record else datetime.now(timezone.utc).isoformat(),
        }

    @staticmethod
    def get_assessment_by_id(assessment_id: str, user_id: str = None) -> dict:
        record = db.session.get(LifestyleAssessment, assessment_id)
        if not record:
            raise NotFoundError(f"Lifestyle assessment '{assessment_id}' not found.")
        if user_id and record.user_id != user_id:
            raise ForbiddenError("You do not have access to this assessment.")
        return record.to_dict()

    @staticmethod
    def delete_assessment(assessment_id: str, user_id: str):
        record = db.session.get(LifestyleAssessment, assessment_id)
        if not record:
            raise NotFoundError(f"Lifestyle assessment '{assessment_id}' not found.")
        if record.user_id != user_id:
            raise ForbiddenError("You do not have access to delete this assessment.")
        db.session.delete(record)
        db.session.commit()

    @staticmethod
    def get_user_history(user_id: str, page: int = 1, per_page: int = 10) -> dict:
        pagination = (
            LifestyleAssessment.query.filter_by(user_id=user_id)
            .order_by(LifestyleAssessment.created_at.desc())
            .paginate(page=page, per_page=per_page, error_out=False)
        )
        return {
            "items": [item.to_dict() for item in pagination.items],
            "total": pagination.total,
            "pages": pagination.pages,
            "page": pagination.page,
            "per_page": pagination.per_page,
        }
