from flask import Flask, render_template, request, url_for, flash, redirect, Response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from datetime import date, datetime, date as date_imp
import os
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()

# Konfigurasi Database - Gunakan PostgreSQL jika DATABASE_URL tersedia

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'the-secret-key')

db = SQLAlchemy(app) 


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(120), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, nullable=False, default=date.today)

with app.app_context():
    db.create_all()

CATEGORIES = ["Food", "Transport", "Utilities", "Health", "Other"]


def parse_date_or_none(s:str):
    if not s:
        return None
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except ValueError: 
        return None

@app.route("/")
def home():

    # Read the quary string 
    start_str = (request.args.get("start") or "").strip()
    end_str = (request.args.get("end") or "").strip()
    select_categories = (request.args.get("category") or "").strip()

    # Parsing
    start_date = parse_date_or_none(start_str)
    end_date = parse_date_or_none(end_str)

    if start_date and end_date and end_date < start_date:
        flash("End date cannot be before start date!", "error")
        start_date = end_date = None
        start_str = end_str = ""

    q = Expense.query
    if start_date:
        q = q.filter(Expense.date >= start_date)
    if end_date:
        q = q.filter(Expense.date <= end_date)
    
    if select_categories:
        q = q.filter(Expense.category == select_categories )

    expenses = q.order_by(Expense.date.desc(), Expense.id.desc()).all()
    total = round(sum(e.amount for e in expenses), 2)

    # Pie Chart Database
    category_q =  db.session.query(Expense.category, func.sum(Expense.amount))

    if start_date:
        category_q = category_q.filter(Expense.date >= start_date)
    if end_date:
        category_q = category_q.filter(Expense.date <= end_date)
    if select_categories:
        category_q = category_q.filter(Expense.category == select_categories)

    category_row = category_q.group_by(Expense.category).all()
    category_labels = [c for c, _ in category_row]
    category_values = [round(float(s or 0), 2) for _, s in category_row]

    # Day Chart
    day_q = db.session.query(Expense.date, func.sum(Expense.amount))

    if start_date:
        day_q = day_q.filter(Expense.date >= start_date)
    if end_date:
        day_q = day_q.filter(Expense.date <= end_date)
    if select_categories:
        day_q = day_q.filter(Expense.category == select_categories)

    day_row = day_q.group_by(Expense.date).order_by(Expense.date).all()  # ✅ GROUP BY date
    day_labels = [d.isoformat() for d, _ in day_row]
    day_values = [round(float(s or 0), 2) for _, s in day_row]

    return render_template("index.html", 
                           expenses=expenses,
                           categories = CATEGORIES,
                           total = total,
                           start_str=start_str,
                           end_str = end_str,
                           today= date.today().isoformat(),
                           selected_category = select_categories,
                           cat_labels = category_labels,
                           cat_values = category_values,
                           day_labels=day_labels,
                           day_values=day_values
                           )

@app.route("/add", methods=["POST"])
def add():
    description = (request.form.get("description") or "").strip()
    amount = (request.form.get("amount") or "").strip()
    category = (request.form.get("category") or "").strip()
    date_str = (request.form.get("date") or "").strip()

    if not description or not amount or not category:
        flash("Please fill description, amount, and the category!", "error")
        return redirect(url_for("home"))

    try:
        amount = float(amount)
        if amount <= 0:
            raise ValueError
    except ValueError:
        flash("Amount must be positive number", "error")
        return redirect(url_for("home"))


    try:
        d = datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else date.today()
    except ValueError:
        d = date.today

    e = Expense(description= description, amount=amount, category=category, date=d)
    db.session.add(e)
    db.session.commit()

    flash("Expense added", "success")
    return redirect(url_for("home"))

@app.route("/delete/<int:expense_id>", methods=["POST"])
def delete(expense_id):
    e = Expense.query.get_or_404(expense_id)
    db.session.delete(e)
    db.session.commit()
    flash("Expense deleted!", "success")
    return redirect(url_for("home"))


@app.route("/export.csv")
def export_csv():
    # Read the quary string 
    start_str = (request.args.get("start") or "").strip()
    end_str = (request.args.get("end") or "").strip()
    select_categories = (request.args.get("category") or "").strip()

    # Parsing
    start_date = parse_date_or_none(start_str)
    end_date = parse_date_or_none(end_str)

    q = Expense.query
    if start_date:
        q = q.filter(Expense.date >= start_date)
    if end_date:
        q = q.filter(Expense.date <= end_date)
    
    if select_categories:
        q = q.filter(Expense.category == select_categories )

    expenses = q.order_by(Expense.date, Expense.id).all()

    lines = ["date, description, category, amount"]

    for e in expenses:
        lines.append(f"{e.date.isoformat()}, {e.description}, {e.category}, {e.amount:.2f}")
    csv_data = "\n".join(lines)

    file_name_start = start_str or "all"
    file_name_end = end_str or "all"

    filename = f"expenses_{file_name_start}_to_{file_name_end}.csv"

    return Response(
        csv_data, 
        headers= {
            "Content-Type": "text/csv",
            "Content-Disposition" : f"attachment; filename = {filename}" 
        }
    )

@app.route("/edit/<int:expense_id>", methods=["GET"])
def edit(expense_id):
    e = Expense.query.get_or_404(expense_id)
    return render_template("edit.html", expense=e, categories=CATEGORIES, today=date_imp.today().isoformat())

@app.route("/edit/<int:expense_id>", methods=["POST"])
def edit_post(expense_id):
    e = Expense.query.get_or_404(expense_id)
    description = (request.form.get("description") or "").strip()
    amount_str = (request.form.get("amount") or "").strip()
    category = (request.form.get("category") or "").strip()
    date_str = (request.form.get("date") or "").strip()

    if not description or not amount_str or not category:
        flash("Please fill description, amount, and the category!", "error")
        return redirect(url_for('edit', expense_id=expense_id))
    
    try:
        amount = float(amount_str)
        if amount <= 0:
            raise ValueError
    except ValueError:
        flash("Amount must be a positive number!", "error")
        return redirect(url_for('edit', expense_id=expense_id))
    
    try:
        d = datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else date_imp.today()
    except ValueError:
        d = date_imp.today()

    e.description = description
    e.amount = amount
    e.category = category
    e.date = d

    db.session.commit()
    flash("Expense Updated!", "success")
    return redirect(url_for('home'))





if __name__ == "__main__":
    app.run(debug=True)