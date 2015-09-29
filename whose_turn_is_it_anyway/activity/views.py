# -*- coding: utf-8 -*-
from flask import (Blueprint, request, render_template, flash, url_for,
                   redirect, session)
from sqlalchemy.sql import func
from flask_login import login_required, current_user

from whose_turn_is_it_anyway.utils import flash_errors

from .forms import CreateActivityForm
from .models import Activity, Participant, Occurrence
from whose_turn_is_it_anyway.extensions import db

blueprint = Blueprint('activities', __name__, url_prefix='/activity', static_folder="../static")


@blueprint.route("/", methods=["GET", "POST"])
@login_required
def overview():

    activity_ids_from_participants = db.session.query(Participant.activity_id).\
        filter(Participant.user_id == current_user.get_id())\
        .all()
    activity_ids_from_creator = db.session.query(Activity.id)\
        .filter(Activity.creator_id == current_user.get_id())\
        .all()
    activity_ids_for_user = list(set(activity_ids_from_participants + activity_ids_from_creator))
    activity_ids_for_user = [t[0] for t in activity_ids_for_user]
    activities = Activity.query.filter(Activity.id.in_(activity_ids_for_user)).all()

    form = CreateActivityForm(request.form)
    if form.validate_on_submit():
        new_activity = Activity.create(name=form.name.data, creator_id=current_user.get_id())
        for participant in form.participants:
            sanitized_participant = participant.data.strip()
            if sanitized_participant:
                Participant.create(name=sanitized_participant, activity_id=new_activity.id)
        if form.current_user_as_participant:
            Participant.create(activity_id=new_activity.id, user_id=current_user.get_id())

        flash("Activity created, You can now start tracking whose turn it is! {}".format(form.participants.data), 'success')
        return redirect(url_for('activities.overview'))
    else:
        flash_errors(form)

    if len(form.participants) == 0:
        # Make sure to have at least one fields in the field list when rendering the page
        form.participants.append_entry("")
    return render_template("activity/overview.html", form=form, activities=activities)


@blueprint.route("/activity/<activity_id>", methods=["GET", "POST"])
@login_required
def activity_detail(activity_id):
    activity = Activity.query.filter_by(id=activity_id).one()

    if int(activity.creator_id) != int(current_user.get_id()):
        flash("Not allowed to access activity", 'warning')
        return redirect(url_for('activities.overview'))

    if request.method == 'POST':
        # TODO validate id

        participant_id = next(request.form.keys())
        Occurrence.create(participant_id=participant_id)
        return redirect(url_for('activities.activity_detail', activity_id=activity_id))
    return render_template("activity/activity.html", activity=activity)

