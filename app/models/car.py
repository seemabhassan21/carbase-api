from datetime import datetime, timezone
from app.extensions import db


class Car(db.Model):
    __tablename__ = 'cars'
    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    @property
    def full_name(self):
        return f"{self.year} {self.make} {self.model}"

    def __str__(self):
        return self.full_name
