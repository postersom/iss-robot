import os
import json
import subprocess

from os.path import join, dirname
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


dotenv_path = join(dirname(__file__), '.env')

setting_json_path = join(dirname(__file__), 'setting.json')
logop_json_path = join(dirname(__file__), 'logop.json')
release_version_json_path = join(dirname(__file__), 'release_version.json')

load_dotenv(dotenv_path)
path = join(dirname(__file__), os.getenv('DATABASE'))
engine = create_engine('sqlite:///'+path, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()


def init_db():
    print("init_db")
    from model.setting import Setting
    from model.status import Status
    from model.test import Test
    from model.log import Log
    from model.userinteraction import Userinteraction
    Base.query = db_session.query_property()
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db_session.commit()


def populate():
    print("populate")
    from model.setting import Setting
    from model.logop import Logop
    from model.releaseversion import ReleaseVersion

    try:
        git_version = subprocess.check_output('/usr/bin/git describe --tag', cwd=dirname(__file__), shell=True).decode('utf-8').strip()
        db_session.add(Setting(name=u'version',
                               title=u'Version',
                               value=git_version,
                               categories=u'lock',
                               order=0))
    except Exception as e:
        print(e)

    with open(setting_json_path) as f:
        data = json.load(f)
        for item in data:
            db_session.add(Setting(name=data[item]['name'],
                                   title=data[item]['title'],
                                   value=data[item]['value'],
                                   categories=data[item]['categories'],
                                   order=data[item]['order']))

    with open(release_version_json_path) as f:
        data = json.load(f)
        [db_session.add(ReleaseVersion(location=i, value=data[i]['release_path_version'])) for i in data]

    with open(logop_json_path) as f:
        data = json.load(f)
        [db_session.add(Logop(name=i, order=data[i]['order'])) for i in data]
    db_session.commit()
