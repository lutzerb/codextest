import csv
from pathlib import Path
from . import db
from .models import Account

def init_db():
    db.create_all()
    if not Account.query.first():
        csv_path = Path('data/ekr.csv')
        if csv_path.exists():
            with csv_path.open(newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                accounts = [Account(number=row['number'], name=row['name'], type=row['type']) for row in reader]
            db.session.add_all(accounts)
            db.session.commit()
