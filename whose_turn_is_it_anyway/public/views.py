# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import (Blueprint, request, render_template, flash, url_for,
                    redirect, session)
from flask_login import login_user, login_required, logout_user

from whose_turn_is_it_anyway.extensions import login_manager
from whose_turn_is_it_anyway.user.models import User
from whose_turn_is_it_anyway.public.forms import LoginForm
from whose_turn_is_it_anyway.user.forms import RegisterForm
from whose_turn_is_it_anyway.utils import flash_errors
from whose_turn_is_it_anyway.database import db

blueprint = Blueprint('public', __name__, static_folder="../static")


@login_manager.user_loader
def load_user(id):
    return User.get_by_id(int(id))


@blueprint.route("/", methods=["GET", "POST"])
def home():
    form = LoginForm(request.form)
    # Handle logging in
    if request.method == 'POST':
        if form.validate_on_submit():
            login_user(form.user, remember=form.remember_me.data)
            flash("You are logged in.", 'success')
            redirect_url = request.args.get("next") or url_for("activities.overview")
            return redirect(redirect_url)
        else:
            flash_errors(form)
    return render_template("public/home.html", form=form)


@blueprint.route('/logout/')
@login_required
def logout():
    logout_user()
    flash('You are logged out.', 'info')
    return redirect(url_for('public.home'))


@blueprint.route("/register/", methods=['GET', 'POST'])
def register():
    register_form = RegisterForm(request.form, csrf_enabled=False)
    if register_form.validate_on_submit():
        new_user = User.create(username=register_form.username.data,
                               email=register_form.email.data,
                               password=register_form.password.data,
                               active=True)
        flash("Thank you for registering. You can now log in.", 'success')
        return redirect(url_for('public.home'))
    else:
        flash_errors(register_form)
    form = LoginForm()
    return render_template('public/register.html', register_form=register_form, form=form)


@blueprint.route("/about/")
def about():
    form = LoginForm(request.form)
    return render_template("public/about.html", form=form)
