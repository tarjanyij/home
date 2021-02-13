from flask import Blueprint, render_template
from flask_sqlalchemy import BaseQuery
from flask_login import login_required, current_user
from cpuinfo import get_cpu_info

from app.models import Temperature, User
from app import db


main = Blueprint('main', __name__)

@main.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('index.html',name=current_user.name)
    else:
        return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

@main.route('/sensortemp')
@login_required
def sensortemp():
    #rows = Temperature.query.filter(thermosensor_id="012033add00d").all()
    #rows = Temperature.query.filter(Temperature.date.like('2020-12-16%')).all()
    row = Temperature.query.filter_by(thermosensor_id="012033add00d").order_by(Temperature.date.desc()).first()

    return render_template('sensortemp.html', name=current_user.name,row = row)

@main.route('/environment')
@login_required
def environment():
    info = get_cpu_info()
    if current_user.is_authenticated:
        return render_template('environment.html',name=current_user.name, info = info)
    else:
        return render_template('environment.html', info = info)
