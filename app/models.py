from datetime import date
from . import db

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(10), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(20))  # asset, liability, equity, income, expense

    def __repr__(self):
        return f"{self.number} {self.name}"

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    entry_date = db.Column(db.Date, default=date.today)
    description = db.Column(db.String(200))
    debit_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    credit_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)

    debit = db.relationship('Account', foreign_keys=[debit_id])
    credit = db.relationship('Account', foreign_keys=[credit_id])

