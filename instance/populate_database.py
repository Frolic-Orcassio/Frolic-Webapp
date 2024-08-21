import time
from flask_sqlalchemy import SQLAlchemy
from Application.models import User, Event, EventWiseOrganizers, Participant, Coordinator, BranchAdmin, Team, TeamWiseMembers
from Application.blueprints.admin import bp
from Application import Role, Branch
import os
import random
from icecream import ic

def pick_and_save_random_picture() -> str:
    """Select a random picture and save it as static asset, return the destination path"""
    pictures_path = './pictures'
    randint = random.randint(0, 999)
    source = os.path.join(pictures_path, f'pic{randint}.jpg')
    file_name = ''.join(str(time.time()).split('.')) + '.jpg'
    destination = os.path.join(str(bp.static_folder), 'profiles', file_name)
    with open(source, 'rb') as src, open(destination, 'wb') as dst: 
        dst.write(src.read())
    return file_name

def populate_db(db: SQLAlchemy):
    u = User(email='branchadmin1@darshan.ac.in',
                    name='branchadmin1',
                    is_authenticated=True,
                    dp=pick_and_save_random_picture(),
                    role=Role.BRANCHADMIN.value)
    ic(u)
    db.session.add(u)
    db.session.commit()

    b = BranchAdmin(branch=Branch.BBA.value, user=u)
    ic(b)
    db.session.add(b)
    db.session.commit()
    
