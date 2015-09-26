# -*- coding: utf-8 -*-
from flask import (Blueprint, request, render_template, flash, url_for,
                   redirect, session)

from flask_login import login_required

from whose_turn_is_it_anyway.user.models import User
from whose_turn_is_it_anyway.utils import flash_errors

blueprint = Blueprint('activities', __name__, url_prefix='/activity', static_folder="../static")


@blueprint.route("/", methods=["GET", "POST"])
@login_required
def overview():

    flash("Woei!", 'success')
    return render_template("activity/overview.html")

