from database import db_session
from model.userinteraction import Userinteraction
from model.swagger.user_interacting import UserInteracting
from connexion import NoContent
import datetime
import logging
import six
import json
import re


def get_interactions():
    q = db_session.query(Userinteraction)
    return [p.dump() for p in q]


def get_interaction(id):
    userinteraction = db_session.query(Userinteraction).filter(
        Userinteraction.id == id).one_or_none()
    return userinteraction.dump() or ('Not found', 404)


def put_interaction(interaction):
    p = db_session.query(Userinteraction).filter(
        Userinteraction.id == interaction['id']).one_or_none()
    id = interaction['id']
    if p is not None:
        logging.info('Updating pet %s..', id)
        p.update(**interaction)
    else:
        logging.info('Creating pet %s..', id)
        interaction['created'] = datetime.datetime.now()
        db_session.add(Userinteraction(**interaction))
    db_session.commit()
    return NoContent, (200 if p is not None else 201)


def delete_interaction(id):
    userinteraction = db_session.query(Userinteraction).filter(
        Userinteraction.id == id).one_or_none()
    if userinteraction is not None:
        logging.info('Deleting pet %s..', id)
        db_session.query(Userinteraction).filter(
            Userinteraction.id == id).delete()
        db_session.commit()
        return NoContent, 204
    else:
        return NoContent, 404


def delete_interaction_by_slot(slot_no):
    try:
        interaction = get_interaction_by_slot(int(slot_no))
        if (interaction):
            delete_interaction(interaction['id'])
        return True
    except Exception as e:
        return e
def get_interaction_by_slot(slot_no):
    userinteraction = db_session.query(Userinteraction).filter(
        Userinteraction.slot_no == slot_no).one_or_none()
    if userinteraction:
        return userinteraction.dump()
    else:
        return None


def add_user_interaction(slot_no, title, message, picture, html, timeout):
    db_session.add(Userinteraction(slot_no=slot_no, title=title, message=message,
                                   picture=picture, html=html, timeout=timeout, created=datetime.datetime.now()))
    db_session.commit()


def create_user_interaction(body):
    request_body = json.loads(body.decode())
    user_interacting = UserInteracting()
    tmp_return_data = user_interacting.return_data

    if not request_body:
        tmp_return_data['error'] = True
        tmp_return_data['data'] = "Not found parameter please check it and try again"

    if not tmp_return_data['error']:
        user_interacting.create_user_interaction()
        slot_no = slot_location_to_slot_no(request_body['slot_location_no'])
        add_user_interaction(int(slot_no), request_body['title'],
                             request_body['message'], request_body['picture'], request_body['html'], int(request_body['timeout']))

    status = 200 if not tmp_return_data['error'] else 400
    tmp_return_data['data'] = "Create user interaction complete" if status == 200 else ""
    return tmp_return_data, status


def user_interaction(slot_location_no):
    user_interacting = UserInteracting()
    tmp_return_data = user_interacting.return_data
    slot_no = slot_location_to_slot_no(slot_location_no)
    user_interacting.user_interaction()
    interaction = get_interaction_by_slot(int(slot_no))
    if not interaction:
        tmp_return_data['error'] = "no user interaction on this slot"
    else:
        if interaction['answer']:
            delete_interaction(interaction['id'])
        else:
            tmp_return_data['error'] = "not answered yet"

    status = 200 if not tmp_return_data['error'] else 400
    tmp_return_data['data'] = interaction if status == 200 else None
    return tmp_return_data, status

def slot_location_to_slot_no(slot_location):
    slot_no = 0
    if(slot_location != ''):
        slot_no = int(re.search(r'\d+', slot_location).group())
    return str(slot_no)