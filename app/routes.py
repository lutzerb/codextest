from flask import render_template, request, redirect, url_for
from . import app, db
from .models import Account, Entry

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/accounts')
def accounts():
    accounts = Account.query.order_by(Account.number).all()
    return render_template('accounts.html', accounts=accounts)

@app.route('/entries', methods=['GET', 'POST'])
def entries():
    accounts = Account.query.order_by(Account.number).all()
    if request.method == 'POST':
        debit_id = request.form['debit']
        credit_id = request.form['credit']
        amount = float(request.form['amount'])
        description = request.form.get('description', '')
        entry = Entry(debit_id=debit_id, credit_id=credit_id, amount=amount, description=description)
        db.session.add(entry)
        db.session.commit()
        return redirect(url_for('entries'))
    entries = Entry.query.order_by(Entry.entry_date.desc()).all()
    return render_template('entries.html', entries=entries, accounts=accounts)

@app.route('/profit_loss')
def profit_loss():
    income_accounts = Account.query.filter(Account.type=='income').all()
    expense_accounts = Account.query.filter(Account.type=='expense').all()
    incomes = []
    expenses = []
    income_total = 0
    expense_total = 0
    for acc in income_accounts:
        amount = db.session.query(db.func.sum(Entry.amount)).filter(Entry.credit_id==acc.id).scalar() or 0
        incomes.append((f"{acc.number} {acc.name}", amount))
        income_total += amount
    for acc in expense_accounts:
        amount = db.session.query(db.func.sum(Entry.amount)).filter(Entry.debit_id==acc.id).scalar() or 0
        expenses.append((f"{acc.number} {acc.name}", amount))
        expense_total += amount
    profit = income_total - expense_total
    return render_template('profit_loss.html', incomes=incomes, expenses=expenses, income_total=income_total, expense_total=expense_total, profit=profit)

@app.route('/balance')
def balance():
    assets = Account.query.filter(Account.type=='asset').all()
    liabilities = Account.query.filter(Account.type=='liability').all()
    asset_items = []
    liability_items = []
    asset_total = 0
    liability_total = 0
    for acc in assets:
        debit = db.session.query(db.func.sum(Entry.amount)).filter(Entry.debit_id==acc.id).scalar() or 0
        credit = db.session.query(db.func.sum(Entry.amount)).filter(Entry.credit_id==acc.id).scalar() or 0
        balance = debit - credit
        asset_items.append({'name': f"{acc.number} {acc.name}", 'amount': balance})
        asset_total += balance
    for acc in liabilities:
        debit = db.session.query(db.func.sum(Entry.amount)).filter(Entry.debit_id==acc.id).scalar() or 0
        credit = db.session.query(db.func.sum(Entry.amount)).filter(Entry.credit_id==acc.id).scalar() or 0
        balance = credit - debit
        liability_items.append({'name': f"{acc.number} {acc.name}", 'amount': balance})
        liability_total += balance
    # align rows for table output
    length = max(len(asset_items), len(liability_items))
    rows = []
    for i in range(length):
        left = asset_items[i] if i < len(asset_items) else None
        right = liability_items[i] if i < len(liability_items) else None
        rows.append((left, right))
    equity = asset_total - liability_total
    return render_template('balance.html', rows=rows, asset_total=asset_total, liability_total=liability_total, equity=equity)

@app.route('/vat')
def vat():
    vat_income = db.session.query(db.func.sum(Entry.amount)).join(Account, Entry.credit_id==Account.id).filter(Account.name.ilike('%Umsatzsteuer%')).scalar() or 0
    vat_expense = db.session.query(db.func.sum(Entry.amount)).join(Account, Entry.debit_id==Account.id).filter(Account.name.ilike('%Vorsteuer%')).scalar() or 0
    vat_due = vat_income - vat_expense
    return render_template('vat.html', vat_income=vat_income, vat_expense=vat_expense, vat_due=vat_due)
