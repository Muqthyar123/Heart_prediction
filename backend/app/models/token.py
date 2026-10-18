import uuid
from datetime import datetime, timezone
from app.extensions import db


class TokenBlocklist(db.Model):
    __tablename__ = "token_blocklist"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    jti = db.Column(db.String(36), unique=True, nullable=False, index=True)
    token_type = db.Column(db.String(10), nullable=False)  # 'access' or 'refresh'
    user_id = db.Column(db.String(36), nullable=True, index=True)
    revoked_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    expires_at = db.Column(db.DateTime, nullable=True)

    def to_dict(self):
        return {
            "jti": self.jti,
            "token_type": self.token_type,
            "revoked_at": self.revoked_at.isoformat() if self.revoked_at else None,
        }
