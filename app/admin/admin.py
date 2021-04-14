from app import db
from app.models import User, Role, UserRoles
from app.admin import bp

from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from flask_sqlalchemy import BaseQuery





@bp.route('/adduser', methods=['GET','POST'])
@login_required
def adduser():
    if request.method == 'GET':
        roles = Role.query.filter().order_by(Role.id).all()
        return render_template('admin/adduser.html',name=current_user.name, roles = roles)
    else:
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        #role = request.form.get('role')
        roleid = request.form.get('role')

        if not name or not email or not password:
            flash('Please fill in all the fields and try again.')
            return redirect(url_for('admin.adduser'))
        else:
            user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

        if user: # if a user is found, we want to redirect back to signup page so user can try again
            flash('Email address already exists')
            return redirect(url_for('admin.adduser'))
        
        # create a new user with the form data. Hash the password so the plaintext version isn't saved.
        new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))
        #new_user.roles.append(Role(rolename=role)) # dokumentáció szerint igy kéne működnie, de a meglévő szerepkör nevét bővítené és ez hiba
        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()
        
        #ez egy menekülö út 
        userrole =UserRoles(user_id = new_user.id, role_id = roleid)
        db.session.add(userrole)
        db.session.commit()
        return redirect(url_for('main.index'))

@bp.route('/edituser', methods=['GET'])
@login_required
def edituser():
    users = User.query.filter().all()
    return render_template('admin/edituser.html',name=current_user.name, users=users)


@bp.route('/edituser', methods=['POST'])
@login_required
def edituser_writedb():
    id = request.form.get('id')
    operate = request.form.get('operate')
    
    if operate == 'modaldata':
        user = User.query.filter(User.id == id)
        data = User.to_collection_dict(user)
        return jsonify(data)

    elif operate =='edit':
        pass
    
@bp.route('/deleteuser', methods=['POST'])
@login_required
def deleteuser():
    id = request.form.get('id')
    User.query.filter_by(id = id).delete()
    db.session.commit()
    users = User.query.filter().all()
    return render_template('admin/edituser.html',name=current_user.name, users=users)


@bp.route('/profile')
@login_required
def profile():
    user = User.query.filter(User.name == current_user.name)  
    return render_template('admin/profile.html', name=current_user.name, user = user)