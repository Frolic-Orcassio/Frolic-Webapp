from flask import Flask, g, redirect, render_template, request, url_for
from instance import IApplicationConfiguration
from sqlalchemy.orm import MappedAsDataclass, DeclarativeBase
from flask_sqlalchemy import SQLAlchemy
from enum import StrEnum, auto
from flask_htmx import HTMX
from functools import wraps

class Base(MappedAsDataclass, DeclarativeBase):
    pass

db: SQLAlchemy = SQLAlchemy(model_class=Base)
htmx = HTMX()

def create_app(config: IApplicationConfiguration, /) -> Flask:
    app: Flask = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config)

    # import Application.error_handlers as errhndl
    # app.register_error_handler(exceptions.HTTPException, errhndl.jsonify_default_errors)
    # app.register_error_handler(exceptions.NotFound, errhndl.handle_notfound_errors)

    from Application.blueprints import admin
    app.register_blueprint(admin.bp)

    htmx.init_app(app)

    db.init_app(app)
    from Application.models import User, Event, EventWiseOrganizers, Participant, BranchAdmin, Coordinator, Team, TeamWiseMembers
    with app.app_context():
        db.create_all()
        if app.debug == True:
            from instance.populate_database import populate_db
            populate_db(db)

    @app.get('/')
    def home():
        return render_template('index.html')
            
    return app


class Role(StrEnum):
    ADMIN = auto()
    BRANCHADMIN = auto()
    ORGANIZER = auto()
    COORDINATOR = auto()
    PARTICIPANT = auto()

class Branch(StrEnum):
    BTECH = auto()
    BCA = auto()
    BBA = auto()
    BSC = auto()
    GENERAL = auto()


def htmx_required(*, redirect_endpoint: str):
    """checks if the reqest is made by htmx, if test fails then redirects to given url"""
    def decorator(view):
        @wraps(view)
        def wrapped_view(**kwargs):
            if not htmx:
                return redirect(url_for(redirect_endpoint))
            return view(**kwargs)
        return wrapped_view
    return decorator

def load_requested_user(*, redirect_endpoint: str):
    """get email from args and query the user with that email from database, if email or user is None then redirect to given url"""
    def decorator(view):
        @wraps(view)
        def wrapped_view(**kwargs):
            email = request.args.get('email')
            if email:
                from Application.models import User
                user = User.query.get(email)
                if user:
                    g.user = user
                    return view(**kwargs)
            return redirect(url_for(redirect_endpoint))
        return wrapped_view
    return decorator
