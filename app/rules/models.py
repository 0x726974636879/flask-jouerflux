from app import db
from app.base_model import Base


class Rule(Base):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    policy_id = db.Column(
        db.Integer, db.ForeignKey("policies.id"), nullable=False
    )

    __table_args__ = (
        db.UniqueConstraint(
            "name", "policy_id", name="rule_name_policy_id_uc"
        ),
    )
    __tablename__ = "rules"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "policy_id": self.policy_id
        }
