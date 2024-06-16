from app import db
from app.base_model import Base


class Policy(Base):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    firewall_id = db.Column(
        db.Integer, db.ForeignKey("firewalls.id"), nullable=False
    )
    rules = db.relationship(
        "Rule", backref="policy", cascade="all, delete-orphan"
    )

    __table_args__ = (
        db.UniqueConstraint(
            "name", "firewall_id", name="policy_name_firewall_id_uc"
        ),
    )
    __tablename__ = "policies"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "firewall_id": self.firewall_id
        }
