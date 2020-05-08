from flask import render_template, flash, redirect, url_for
from app.auth.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, login_required
from app.models import Users
from flask_login import logout_user
from app import db
from app.auth import bp


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(user)
        # login_user(user, remember=form.remember_me.data)
        return redirect(url_for('main.index'))
    return render_template('basic_form.html', title='Sign In', form=form)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Users(username=form.username.data, email=form.email.data, nborhood=form.nborhood.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!', 'success')
        return redirect(url_for('auth.login'))
    return render_template('basic_form.html', title='Register', form=form)


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))