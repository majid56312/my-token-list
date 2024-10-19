from flask import Blueprint, render_template, redirect, url_for, flash
from flask_security import login_required, current_user
from forms import RegisterForm, LoginForm, TradeForm
from models import db, User, Currency

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('base.html')

@main.route('/dashboard')
@login_required
def dashboard():
    currencies = Currency.query.all()
    return render_template('dashboard.html', currencies=currencies)

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('کاربر جدید با موفقیت ثبت شد!')
        return redirect(url_for('main.index'))
    return render_template('register.html', form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Authentication logic
        pass
    return render_template('login.html', form=form)

@main.route('/trade', methods=['GET', 'POST'])
@login_required
def trade():
    form = TradeForm()
    form.currency.choices = [(currency.id, currency.name) for currency in Currency.query.all()]
    if form.validate_on_submit():
        # Logic to handle trade
        flash('معامله با موفقیت انجام شد!')
        return redirect(url_for('main.dashboard'))
    return render_template('trade.html', form=form)
