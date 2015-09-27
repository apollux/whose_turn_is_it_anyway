# -*- coding: utf-8 -*-
from flask import (Blueprint, request, render_template, flash, url_for,
                   redirect, session)

from flask_login import login_required, current_user

from whose_turn_is_it_anyway.utils import flash_errors

from .forms import CreateActivityForm
from .models import Activity

blueprint = Blueprint('activities', __name__, url_prefix='/activity', static_folder="../static")


@blueprint.route("/", methods=["GET", "POST"])
@login_required
def overview():
    flash("Woei!", 'success')

    form = CreateActivityForm(request.form)
    form.participants.append_entry("tessthsthstt")
    if form.validate_on_submit():
        new_activity = Activity.create(name=form.name.data, creator_id=current_user.get_id())
        flash("Activity created, You can now start tracking whose turn it is! {}".format(form.participants.data), 'success')
        return redirect(url_for('activities.overview'))
    else:
        flash_errors(form)
    return render_template("activity/overview.html", form=form)

