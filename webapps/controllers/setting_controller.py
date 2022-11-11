from database import db_session
from model.setting import Setting
from model.logop import Logop
from model.releaseversion import ReleaseVersion
from connexion import NoContent
import datetime
import logging


def get_settings(limit):
    q = db_session.query(Setting).order_by(Setting.categories.asc(), Setting.order.asc())
    return [p.dump() for p in q][:limit]


def get_setting(id):
    setting = db_session.query(Setting).filter(
        Setting.id == id).one_or_none()
    return setting.dump() or ('Not found', 404)


def get_setting_by_name(name):
    setting = db_session.query(Setting).filter(
        Setting.name == name).one_or_none()
    if setting:
        return setting.dump()
    else:
        return ('Not found', 404)


def put_setting(setting):
    p = db_session.query(Setting).filter(
        Setting.id == setting['id']).one_or_none()
    id = setting['id']
    if p is not None:
        logging.info('Updating pet %s..', id)
        p.update(**setting)
    else:
        logging.info('Creating pet %s..', id)
        setting['created'] = datetime.datetime.now()
        db_session.add(Setting(**setting))
    db_session.commit()
    return NoContent, (200 if p is not None else 201)


def delete_setting(id):
    setting = db_session.query(Setting).filter(Setting.id == id).one_or_none()
    if setting is not None:
        logging.info('Deleting pet %s..', id)
        db_session.query(Setting).filter(Setting.id == id).delete()
        db_session.commit()
        return NoContent, 204
    else:
        return NoContent, 404


def save_all_setting(data):
    for k, v in data.items():
        p = db_session.query(Setting).filter(
            Setting.name == k).one_or_none()
        if p is not None:
            if p.name == 'slot':
                if v.isnumeric() and int(v) > 0:
                    p.value = v
                else:
                    logging.info('Set slot error')
                    p.value = 1
            else:
                p.value = v
            logging.info('Updating Setting')
        else:
            setting = Setting(name=item['name'], title=item['name'], value=item['value'], categories=u'default',
                              order=99)
            logging.info('Creating Setting')
            setting['created'] = datetime.datetime.now()
            db_session.add(setting)
        db_session.commit()
    return NoContent, (200 if p is not None else 201)


def get_logop(limit):
    q = db_session.query(Logop).order_by(Logop.order.asc())
    return [p.dump() for p in q][:limit]


def put_logop(logop):
    p = db_session.query(Logop).filter(Logop.id == logop['id']).one_or_none()
    id = logop['id']
    if p is not None:
        logging.info('Updating pet %s..', id)
        p.update(**logop)
    else:
        logging.info('Creating pet %s..', id)
        db_session.add(Logop(**logop))
    db_session.commit()
    return NoContent, (200 if p is not None else 201)


def delete_logop(name):
    logop = db_session.query(Logop).filter(Logop.name == name).one_or_none()
    if logop is not None:
        logging.info('Deleting pet %s..', name)
        db_session.query(Logop).filter(Logop.name == name).delete()
        db_session.commit()
        return NoContent, 204
    else:
        return NoContent, 404


def get_release_versions(limit):
    q = db_session.query(ReleaseVersion).order_by(ReleaseVersion.id.asc())
    return [p.dump() for p in q][:limit]


def get_release_version_by_location(location):
    release_version = db_session.query(ReleaseVersion).filter(
        ReleaseVersion.location == location).one_or_none()
    if release_version:
        return release_version.dump()
    else:
        return ('Not found', 404)


def put_release_version(code_version):
    p = db_session.query(ReleaseVersion).filter(
        ReleaseVersion.location == code_version['location']).one_or_none()
    location = code_version['location']
    if p is not None:
        logging.info('Updating pet %s..', location)
        p.update(**code_version)
    else:
        logging.info('Creating pet %s..', location)
        db_session.add(ReleaseVersion(**code_version))
    db_session.commit()
    return NoContent, (200 if p is not None else 201)
