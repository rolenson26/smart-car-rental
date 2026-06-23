from database import db


class Membership(db.Model):

    __tablename__ = "memberships"

    membership_id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(50),
        nullable=False
    )

    price = db.Column(
        db.Float,
        nullable=False
    )

    benefits = db.Column(
        db.String(255)
    )