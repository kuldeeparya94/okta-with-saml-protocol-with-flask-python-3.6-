# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, redirect, url_for, render_template, session
from flask_login import login_required, logout_user, UserMixin

blueprint = Blueprint('user', __name__, template_folder='templates')
user_store = {}


@blueprint.route('/api/user', methods=('GET',))
def get_user():
    return "my name is Dummy"


@blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home.main_page"))


@blueprint.route("/user")
@login_required
def user():
    return render_template('user.html', session=session)


class User(UserMixin):
    def __init__(self, user_id, _user_store=None):
        user = {}
        self.id = None
        self.first_name = None
        self.last_name = None
        try:
            user = _user_store[user_id]
            print('----------')
            print(user)
            self.id = unicode(user_id)
            self.first_name = user['first_name']
            self.last_name = user['last_name']
        except:
            pass

