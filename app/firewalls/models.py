from app import db
from app.base_model import Base


class Firewall(Base):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    policies = db.relationship(
        "Policy", backref="firewall", cascade="all, delete-orphan"
    )

    __tablename__ = "firewalls"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }
