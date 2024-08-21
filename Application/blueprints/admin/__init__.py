import time
from flask import Blueprint, g, redirect, render_template, url_for, jsonify, request
from Application import htmx_required, Role, db, load_requested_user
from werkzeug import exceptions
from dataclasses import asdict
from Application.models import User
from icecream import ic
import os
from pydantic import BaseModel, ValidationError

bp = Blueprint('Admin', 
               __name__, 
               url_prefix='/admin', 
               static_folder='static', 
               template_folder='templates')


@bp.get('/all-users')
def index():
    return render_template('admin/index.html', Role=Role)

@bp.delete('/delete-user')
@htmx_required(redirect_endpoint='Admin.index')
@load_requested_user(redirect_endpoint='Admin.index')
def delete_user():
    time.sleep(2)
    user = g.user
    if user.dp: os.remove(os.path.join(bp.static_folder, 'profiles', user.dp))  
    db.session.delete(user)
    db.session.commit()    
    return "", {"HX-Reswap":"none", "HX-Trigger-After-Settle":"userDeleted"}


@bp.patch('/patch-user')
@htmx_required(redirect_endpoint='Admin.index')
@load_requested_user(redirect_endpoint='Admin.index') # a little bit unoptimized because we will hit db no matter the validation of input but not a security concern
def update_user():
    time.sleep(2)
    try:
        if (data:=request.form.get('role')) not in Role:
            return "", 404
        user = g.user
        user.role = data
        db.session.add(user)
        db.session.commit()
        return "", {"HX-Reswap":"none", "HX-Trigger-After-Settle":"userDeleted"}
    except ValidationError:
        return redirect(url_for('Admin.index'))

    


@bp.get('/ajax/all-users')
def ajax_users():
    users = [[u.dp, u.name, u.email, u.role, u.is_authenticated] for u in User.query.all()]
    return {"data": users}

@bp.get('/events')
@htmx_required(redirect_endpoint='Admin.index')
def events():
    return render_template('admin/main/events.html')


@bp.get('/create-event')
@htmx_required(redirect_endpoint='Admin.index')
def create_event():
    return render_template('admin/main/create-event.html'), {"HX-Trigger-After-Settle":"createEditor"}

bp.add_url_rule('/', endpoint='root', view_func=lambda: redirect(url_for('Admin.index')))