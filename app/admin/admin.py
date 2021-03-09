from app import db
from app.models import User
from app.admin import bp

from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from flask_sqlalchemy import BaseQuery





@bp.route('/adduser', methods=['GET','POST'])
@login_required
def adduser():
    if request.method == 'GET':
        return render_template('admin/adduser.html',name=current_user.name)
    else:
        return redirect(url_for('main.index'))

@bp.route('/edituser', methods=['GET'])
@login_required
def edituser():
    users = User.query.filter().all()
    return render_template('admin/edituser.html',name=current_user.name, users=users)

@bp.route('/profile')
@login_required
def profile():
    user = User.query.filter_by(User.name == current_user.name).first()    
    return render_template('admin/profile.html', name=current_user.name, user = user)