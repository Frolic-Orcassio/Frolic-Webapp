import time
from flask import Blueprint, redirect, render_template, url_for
from Application import htmx_required
from werkzeug import exceptions

bp = Blueprint('Admin', 
               __name__, 
               url_prefix='/admin', 
               static_folder='static', 
               template_folder='templates')

@bp.get('/all-users')
def index():
    return render_template('admin/index.html')

@bp.get('/ajax/all-users')
def ajax_users():
    # time.sleep(2)
    return {"data":[['Profile1', 'Soham', 'sohamjobanputra7@gmail.com', 'admin', 'yes'],
                    ['Profile2', 'Soham', 'sohamjobanputra7@gmail.com', 'admin', 'no']
                    ]}

@bp.get('/events')
@htmx_required(redirect_endpoint='Admin.index')
def events():
    return render_template('admin/main/events.html')


@bp.get('/create-event')
@htmx_required(redirect_endpoint='Admin.index')
def create_event():
    return render_template('admin/main/create-event.html'), {"HX-Trigger-After-Settle":"createEditor"}

bp.add_url_rule('/', endpoint='root', view_func=lambda: redirect(url_for('Admin.index')))