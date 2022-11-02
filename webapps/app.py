from flask_socketio import SocketIO
import connexion
import datetime
import logging
from flask import (Flask, render_template, request, redirect,
                   url_for, abort, flash, send_from_directory, send_file, g)


from database import db_session
import database
import time

from datetime import timezone
from controllers.setting_controller import *
from controllers.test_controller import *
from controllers.status_controller import *
from controllers.log_controller import *
from controllers.userinteraction_controller import *
from model.setting import Setting
from os.path import join, dirname
import os
from dotenv import load_dotenv

from model.swagger.testing import Testing
from robot.parsing.model import TestData

import gitlab
import socket
import paramiko
import socket
import sys
import subprocess

import ast
import tarfile
import zipfile
import gzip
import requests

import json

from glob import glob
import posixpath
from itertools import product
import shutil

# Create .env file path.
dotenv_path = join(dirname(__file__), '.env')

# Create json file path.
setting_json_path = join(dirname(__file__), 'setting.json')
logop_json_path = join(dirname(__file__), 'logop.json')
release_version_json_path = join(dirname(__file__), 'release_version.json')

load_dotenv(dotenv_path)

logging.basicConfig(level=logging.INFO)

# Path of project
dir_path = os.path.dirname(os.path.abspath(__file__))
dist_release_path = '/home/export/release/'
robot_root_path = '/opt/Robot/'


app = connexion.App(__name__, specification_dir='./')
app.add_api('swagger.yaml')
# set the WSGI application callable to allow using uWSGI:
# uwsgi --http :8080 -w app
application = app.app
application.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
application.secret_key = os.urandom(16)
database.init_db()
# socketio
# create a Socket.IO server
socketio = SocketIO(application)

color_testing = "f9c74f"
color_failing = "f8961e"
color_failed  =  "f94144"
color_aborted = "f3722c"
color_passes = "90be6d"

# Create a URL route in our application for "/"
@app.route('/')
def home():
    """
    This function just responds to the browser ULR
    localhost:5000/
    :return:        the rendered template 'home.html'
    """
    info = dict()
    settings = get_settings(100)
    for item in settings:
        if item["name"] == 'slot':
            info['slot'] = int(item["value"])
        elif item["name"] == 'chamber':
            info['chamber'] = int(item["value"])
        elif item["name"] == 'product_name':
            info['product_name'] = item["value"]
        elif item["name"] == 'operation':
            info['operation'] = item["value"]
        elif item["name"] == 'chassis_name':
            info['chassis_name'] = item["value"]
        elif item["name"] == 'station':
            info['station'] = item["value"]
        elif item["name"] == 'parameter':
            info['parameter'] = item["value"]
        elif item["name"] == 'interval':
            info['interval'] = int(item["value"])
        elif item["name"] == 'log_template':
            info['log_template'] = item["value"]
        elif item["name"] == 'version':
            info['version'] = item["value"]
        elif item["name"] == 'model_test':
            info['model_test'] = item["value"]

    block_title = '{}_{}'.format(info['product_name'], info['station'])

    info_versions = list()
    release_versions = get_release_versions(100)
    for item in release_versions:
        info_versions.append(item['value'])

    logops = get_logop(100)

    tests = get_tests(100)

    chambers = list()
    test_slot = list()

    test_id = 0

    # print('chamber={}'.format(info['chamber']))
    # print('product_name={}'.format(info['product_name']))

    for i in range(1, info['chamber']+1):
        chambers.append(dict())

    for i in range(1, info['slot']+1):
        test_slot.append(dict())
    statuses = get_statuses(100)

    if info['model_test'] == "sub-slot":
        # print(info['chassis_name'])
        for item in tests:
            # print("Check all item : " + json.dumps(item))
            item["statuses"] = sorted(
                item["statuses"], key=lambda i: i['id'], reverse=True)
            item["test_info"] = dict()
            item["test_info"]["color"] = color_testing
            if len(item["statuses"]) > 0:
                # set created time from first test case created
                item["test_info"]["created"] = item["statuses"][-1]["created"]
                # remove timezone string
                if ":" == item["test_info"]["created"][-3:-2]:
                    item["test_info"]["created"] = item["test_info"]["created"][:-3] + \
                        item["test_info"]["created"][-2:]
                if ":" == item["statuses"][0]["created"][-3:-2]:
                    item["statuses"][0]["created"] = item["statuses"][0]["created"][:-3] + \
                        item["statuses"][0]["created"][-2:]
                # print("Status :: " + item["statuses"][0]["status"])
                # check last status not end suite(still testing)
                if item["statuses"][0]["status"] != "end_suite":
                    # loop to find failing
                    item["test_info"]["status"] = "Testing"
                    item["test_info"]["color"] = color_testing
                    for test_case in item["statuses"]:
                        # if end testcase  and message is fail
                        if test_case["status"] == "end_test" and test_case["message"].split(':')[1][:4] == "FAIL":
                            item["test_info"]["status"] = "failing"
                            item["test_info"]["color"] = color_failing
                            break

                    item["test_info"]["test_case"] = item["statuses"][0]["message"]
                    created_time = datetime.datetime.strptime(
                        item["test_info"]["created"], "%Y-%m-%dT%H:%M:%S.%f%z")
                    # get timezone info
                    tz = datetime.datetime.now(
                        datetime.timezone.utc).astimezone().tzinfo
                    # change time object to use same timezone and differential
                    elapsed_time = datetime.datetime.now(
                        tz) - created_time.replace(tzinfo=tz)
                    # remove millisecond
                    item["test_info"]["elapsed_time"] = str(
                        elapsed_time).split('.')[0]
                else:
                    created_time = datetime.datetime.strptime(
                        item["test_info"]["created"], "%Y-%m-%dT%H:%M:%S.%f%z")
                    finished_time = datetime.datetime.strptime(
                        item["statuses"][0]["created"], "%Y-%m-%dT%H:%M:%S.%f%z")
                    elapsed_time = finished_time - created_time
                    item["test_info"]["elapsed_time"] = str(
                        elapsed_time).split('.')[0]
                    print(item["statuses"][1]["message"])
                    try:
                        item["test_info"]["status"] = item["statuses"][1]["message"].split(
                            ':')[1].strip().split(' ')[0].strip()
                    except Exception as e:
                        item["test_info"]["status"] = "FAIL"
                        print(e)

                    # print("Check item status:: " + item["test_info"]["status"])

                    if item["test_info"]["status"] == "FAIL":
                        length = (len(item["statuses"]))

                        # for test_case in reversed(item["statuses"]):  # loop item status to find first error message
                        for z in reversed(range(length)):
                            # print(z, end=" ")
                            print(item["statuses"][z])

                            if item["statuses"][z]["status"] == "end_test" and item["statuses"][z]["message"].split(':')[1][:5] == "ABORT":
                                item["test_info"]["created"] = item["statuses"][z]["message"].split(':')[
                                    1][:5]
                                print('------test_abort' +
                                      item["test_info"]["created"])
                                test_id = -1
                                break
                            elif item["statuses"][z]["status"] == "end_test" and item["statuses"][z]["message"].split(':')[1][:4] == "FAIL":
                                item["test_info"]["message"] = item["statuses"][z]["message"].replace(
                                    "Result:FAIL ", "")
                                test_id = z
                                print('######test_case_fail_name######' +
                                      item["test_info"]["message"])
                                print(
                                    '######test_case_fail_nameID######'+str(test_id))
                                break

                        for x in range(length):

                            print('######ID######'+str(test_id))
                            if test_id == -1:
                                print('######ABORT######'+str(test_id))

                            elif x == test_id+1:
                                # item["test_info"]["message"] = test_case["message"].replace([1][:2],"")
                                print('######ID******'+str(x))
                                item["test_info"]["test_db"] = item["statuses"][x]["message"]

                                break

                        item["test_info"]["status"] = "failed"
                        item["test_info"]["color"] = color_failed
                    elif item["test_info"]["status"] == "PASS":
                        item["test_info"]["status"] = "passes"
                        item["test_info"]["color"] = color_passes
                    elif item["test_info"]["status"] == "ABORT":
                        item["test_info"]["status"] = "aborted"
                        item["test_info"]["color"] = color_aborted
                    else:
                        item["test_info"]["status"] = "failed"
                        item["test_info"]["color"] = color_failed

                slot_location = info['chassis_name'] + \
                    str(item["statuses"][0]["slot_no"])
                release_version = get_release_version_by_location(
                    slot_location)
                item["code_version"] = release_version['value']

            position = item["location"]
            position = position.split("_")
            if int(position[0]) > info['slot']:
                chambers[int(position[0])-info['slot']-1] = item
            elif len(position) > 1:
                test_slot[int(position[0])-1][int(position[1])] = item
            else:
                test_slot[int(position[0])-1][0] = item

        for index, tss in enumerate(test_slot):
            status_test = ""
            for ts in tss:
                if (tss[ts]["test_info"]):
                    if tss[ts]["test_info"]["status"] == "Testing":
                        status_test = "Testing"
                    elif tss[ts]["test_info"]["status"] == "aborted" and status_test != "Testing":
                        status_test = "aborted"
                    elif tss[ts]["test_info"]["status"] == "failed" and status_test != "Testing" and status_test != "aborted":
                        status_test = "failed"
                    elif tss[ts]["test_info"]["status"] == "passes" and status_test != "Testing" and status_test != "aborted" and status_test != "failed":
                        status_test = "passes"
            if status_test != "":
                test_slot[index]["status"] = status_test

        if len(tests) > 0:
            user_interactions = get_interactions()
            for interact in user_interactions:
                tmp_slot = int(interact["slot_no"])
                test_slot[tmp_slot-1]["user_interactions"] = interact
        return render_template('home_SubSlot.html', chambers=chambers, info=info, tests=test_slot, statuses=statuses, info_versions=info_versions, logops=logops, block_title=block_title)
    elif info['model_test'] == "bi":
        for i in range(1, info['slot']+1):
            test_slot.append(dict())
        for item in tests:
            # print("Check all item : " + json.dumps(item))
            item["statuses"] = sorted(
                item["statuses"], key=lambda i: i['id'], reverse=True)
            item["test_info"] = dict()
            if len(item["statuses"]) > 0:
                # set created time from first test case created
                item["test_info"]["created"] = item["statuses"][-1]["created"]
                # remove timezone string
                if ":" == item["test_info"]["created"][-3:-2]:
                    item["test_info"]["created"] = item["test_info"]["created"][:-3] + \
                        item["test_info"]["created"][-2:]
                if ":" == item["statuses"][0]["created"][-3:-2]:
                    item["statuses"][0]["created"] = item["statuses"][0]["created"][:-3] + \
                        item["statuses"][0]["created"][-2:]
                # print("Status :: " + item["statuses"][0]["status"])
                # check last status not end suite(still testing)
                if item["statuses"][0]["status"] != "end_suite":
                    # loop to find failing
                    item["test_info"]["status"] = "Testing"
                    item["test_info"]["color"] = color_testing
                    for test_case in item["statuses"]:
                        # if end testcase  and message is fail
                        if test_case["status"] == "end_test" and test_case["message"].split(':')[1][:5] == "ABORT":
                            item["test_info"]["status"] = "aborted"
                            item["test_info"]["color"] = color_aborted
                            break
                        if test_case["status"] == "end_test" and test_case["message"].split(':')[1][:4] == "FAIL":
                            item["test_info"]["status"] = "failing"
                            item["test_info"]["color"] = color_failing
                            break

                    item["test_info"]["test_case"] = item["statuses"][0]["message"]
                    created_time = datetime.datetime.strptime(
                        item["test_info"]["created"], "%Y-%m-%dT%H:%M:%S.%f%z")
                    # get timezone info
                    tz = datetime.datetime.now(
                        datetime.timezone.utc).astimezone().tzinfo
                    # change time object to use same timezone and differential
                    elapsed_time = datetime.datetime.now(
                        tz) - created_time.replace(tzinfo=tz)
                    # remove millisecond
                    item["test_info"]["elapsed_time"] = str(
                        elapsed_time).split('.')[0]
                else:
                    created_time = datetime.datetime.strptime(
                        item["test_info"]["created"], "%Y-%m-%dT%H:%M:%S.%f%z")
                    finished_time = datetime.datetime.strptime(
                        item["statuses"][0]["created"], "%Y-%m-%dT%H:%M:%S.%f%z")
                    elapsed_time = finished_time - created_time
                    item["test_info"]["elapsed_time"] = str(
                        elapsed_time).split('.')[0]
                    print(item["statuses"][1]["message"])
                    try:
                        item["test_info"]["status"] = item["statuses"][1]["message"].split(
                            ':')[1].strip().split(' ')[0].strip()
                    except Exception as e:
                        item["test_info"]["status"] = "FAIL"
                        print(e)

                    # print("Check item status:: " + item["test_info"]["status"])

                    if item["test_info"]["status"] == "FAIL":
                        item["test_info"]["status"] = "failed"
                        item["test_info"]["color"] = color_failed
                        length = (len(item["statuses"]))

                        # for test_case in reversed(item["statuses"]):  # loop item status to find first error message
                        for z in reversed(range(length)):
                            print(z, end=" ")
                            print(item["statuses"][z])

                            if item["statuses"][z]["status"] == "end_test" and item["statuses"][z]["message"].split(':')[1][:5] == "ABORT":
                                item["test_info"]["created"] = item["statuses"][z]["message"].split(':')[
                                    1][:5]
                                print('------test_abort' +
                                      item["test_info"]["created"])
                                test_id = -1
                                item["test_info"]["status"] = "aborted"
                                item["test_info"]["color"] = color_aborted
                                break
                            elif item["statuses"][z]["status"] == "end_test" and item["statuses"][z]["message"].split(':')[1][:4] == "FAIL":
                                item["test_info"]["message"] = item["statuses"][z]["message"].replace(
                                    "Result:FAIL ", "")
                                test_id = z
                                print('######test_case_fail_name######' +
                                      item["test_info"]["message"])
                                print(
                                    '######test_case_fail_nameID######'+str(test_id))
                                break

                        for x in range(length):

                            print('######ID######'+str(test_id))
                            if test_id == -1:
                                print('######ABORT######'+str(test_id))

                            elif x == test_id+1:
                                # item["test_info"]["message"] = test_case["message"].replace([1][:2],"")
                                print('######ID******'+str(x))
                                item["test_info"]["test_db"] = item["statuses"][x]["message"]

                                break

                    elif item["test_info"]["status"] == "PASS":
                        item["test_info"]["status"] = "passes"
                        item["test_info"]["color"] = color_passes

                        print("######PASS#########")

                        length = (len(item["statuses"]))
                        for z in reversed(range(length)):
                            if item["statuses"][z]["status"] == "end_test" and item["statuses"][z]["message"].split(':')[1][:4] == "FAIL":
                                item["test_info"]["status"] = "failed"
                                item["test_info"]["color"] = color_failed
                                item["test_info"]["test_case"] = item["statuses"][z+1]["message"]
                                item["test_info"]["message"] = item["statuses"][z]["message"].replace(
                                    "Result:FAIL ", "")
                                item["test_info"]["test_db"] = item["statuses"][z+1]["message"]
                                break

                    elif item["test_info"]["status"] == "ABORT":
                        item["test_info"]["status"] = "aborted"
                        item["test_info"]["color"] = color_aborted
                    else:
                        item["test_info"]["status"] = "failed"
                        item["test_info"]["color"] = color_failed

                print('item : {}'.format(item))
                # position = item["location"]
                if(int(item["location"]) > info['slot']):
                    slot_location = 'chamber{}'.format(
                        str(item["statuses"][0]["slot_no"]))
                    release_version = get_release_version_by_location(
                        slot_location)
                    item["code_version"] = release_version['value']
                else:
                    slot_location = info['chassis_name'] + \
                        str(item["statuses"][0]["slot_no"])
                    release_version = get_release_version_by_location(
                        slot_location)
                    item["code_version"] = release_version['value']
            if(int(item["location"]) > info['slot']):
                chambers[int(item["location"]) - info['slot'] - 1] = item
            else:
                test_slot[int(item["location"])-1] = item
        if len(tests) > 0:
            user_interactions = get_interactions()
            for interact in user_interactions:
                tmp_slot = int(interact["slot_no"])
                test_slot[tmp_slot-1]["user_interactions"] = interact
            print(test_slot)
        return render_template('home_BI.html', chambers=chambers, info=info, tests=test_slot, statuses=statuses, info_versions=info_versions, logops=logops, block_title=block_title)
    else:
        for item in tests:
            # print("Check all item : " + json.dumps(item))
            item["statuses"] = sorted(
                item["statuses"], key=lambda i: i['id'], reverse=True)
            item["test_info"] = dict()
            if len(item["statuses"]) > 0:
                # set created time from first test case created
                item["test_info"]["created"] = item["statuses"][-1]["created"]
                # remove timezone string
                if ":" == item["test_info"]["created"][-3:-2]:
                    item["test_info"]["created"] = item["test_info"]["created"][:-3] + \
                        item["test_info"]["created"][-2:]
                if ":" == item["statuses"][0]["created"][-3:-2]:
                    item["statuses"][0]["created"] = item["statuses"][0]["created"][:-3] + \
                        item["statuses"][0]["created"][-2:]
                # print("Status :: " + item["statuses"][0]["status"])
                # check last status not end suite(still testing)
                if item["statuses"][0]["status"] != "end_suite":
                    # loop to find failing
                    item["test_info"]["status"] = "Testing"
                    item["test_info"]["color"] = color_testing
                    for test_case in item["statuses"]:
                        # if end testcase  and message is fail
                        if test_case["status"] == "end_test" and test_case["message"].split(':')[1][:5] == "ABORT":
                            item["test_info"]["status"] = "aborted"
                            item["test_info"]["color"] = color_aborted

                            break
                        if test_case["status"] == "end_test" and test_case["message"].split(':')[1][:4] == "FAIL":
                            item["test_info"]["status"] = "failing"
                            item["test_info"]["color"] = color_failing
                            break

                    item["test_info"]["test_case"] = item["statuses"][0]["message"]
                    created_time = datetime.datetime.strptime(
                        item["test_info"]["created"], "%Y-%m-%dT%H:%M:%S.%f%z")
                    # get timezone info
                    tz = datetime.datetime.now(
                        datetime.timezone.utc).astimezone().tzinfo
                    # change time object to use same timezone and differential
                    elapsed_time = datetime.datetime.now(
                        tz) - created_time.replace(tzinfo=tz)
                    # remove millisecond
                    item["test_info"]["elapsed_time"] = str(
                        elapsed_time).split('.')[0]
                else:
                    created_time = datetime.datetime.strptime(
                        item["test_info"]["created"], "%Y-%m-%dT%H:%M:%S.%f%z")
                    finished_time = datetime.datetime.strptime(
                        item["statuses"][0]["created"], "%Y-%m-%dT%H:%M:%S.%f%z")
                    elapsed_time = finished_time - created_time
                    item["test_info"]["elapsed_time"] = str(
                        elapsed_time).split('.')[0]
                    print("Status message : " + item["statuses"][1]["message"])
                    try:
                        item["test_info"]["status"] = item["statuses"][1]["message"].split(
                            ':')[1].strip().split(' ')[0].strip()
                    except Exception as e:
                        item["test_info"]["status"] = "FAIL"
                        print(e)

                    # print("Check item status:: " + item["test_info"]["status"])

                    if item["test_info"]["status"] == "FAIL":
                        item["test_info"]["status"] = "failed"
                        item["test_info"]["color"] = color_failed
                        length = (len(item["statuses"]))

                        # for test_case in reversed(item["statuses"]):  # loop item status to find first error message
                        for z in reversed(range(length)):
                            print(z, end=" ")
                            print(item["statuses"][z])

                            if item["statuses"][z]["status"] == "end_test" and item["statuses"][z]["message"].split(':')[1][:5] == "ABORT":
                                item["test_info"]["created"] = item["statuses"][z]["message"].split(':')[
                                    1][:5]
                                print('------test_abort' +
                                      item["test_info"]["created"])
                                test_id = -1
                                item["test_info"]["test_case"] = item["statuses"][z+1]["message"]
                                item["test_info"]["status"] = "aborted"
                                item["test_info"]["color"] = color_aborted
                                break
                            elif item["statuses"][z]["status"] == "end_test" and item["statuses"][z]["message"].split(':')[1][:4] == "FAIL":
                                item["test_info"]["message"] = item["statuses"][z]["message"].replace(
                                    "Result:FAIL ", "")
                                test_id = z
                                item["test_info"]["test_case"] = item["statuses"][z+1]["message"]
                                print('######test_case_fail_name######' +
                                      item["test_info"]["message"])
                                print(
                                    '######test_case_fail_nameID######'+str(test_id))
                                break

                        for x in range(length):

                            print('######ID######'+str(test_id))
                            if test_id == -1:
                                print('######ABORT######'+str(test_id))

                            elif x == test_id+1:
                                # item["test_info"]["message"] = test_case["message"].replace([1][:2],"")
                                print('######ID******'+str(x))
                                item["test_info"]["test_db"] = item["statuses"][x]["message"]

                                break

                    elif item["test_info"]["status"] == "PASS":
                        item["test_info"]["status"] = "passes"
                        item["test_info"]["color"] = color_passes

                        print("######PASS#########")

                        length = (len(item["statuses"]))
                        for z in reversed(range(length)):
                            if item["statuses"][z]["status"] == "end_test" and item["statuses"][z]["message"].split(':')[1][:4] == "FAIL":
                                item["test_info"]["status"] = "failed"
                                item["test_info"]["color"] = color_failed
                                item["test_info"]["test_case"] = item["statuses"][z+1]["message"]
                                item["test_info"]["message"] = item["statuses"][z]["message"].replace(
                                    "Result:FAIL ", "")
                                item["test_info"]["test_db"] = item["statuses"][z+1]["message"]
                                break

                    elif item["test_info"]["status"] == "ABORT":
                        item["test_info"]["status"] = "aborted"
                        item["test_info"]["color"] = color_aborted
                    else:
                        item["test_info"]["status"] = "failed"
                        item["test_info"]["color"] = color_failed

                # position = item["location"]
                if(int(item["location"]) > info['slot']):
                    slot_location = 'chamber{}'.format(
                        str(item["statuses"][0]["slot_no"]))
                    release_version = get_release_version_by_location(
                        slot_location)
                    item["code_version"] = release_version['value']
                else:
                    slot_location = info['chassis_name'] + \
                        str(item["statuses"][0]["slot_no"])
                    release_version = get_release_version_by_location(
                        slot_location)
                    item["code_version"] = release_version['value']
            if(int(item["location"]) > info['slot']):
                chambers[int(item["location"]) - info['slot'] - 1] = item
            else:
                test_slot[int(item["location"])-1] = item
        if len(tests) > 0:
            user_interactions = get_interactions()
            for interact in user_interactions:
                tmp_slot = int(interact["slot_no"])
                test_slot[tmp_slot-1]["user_interactions"] = interact
            print(test_slot)

        print(chambers)

        return render_template('home.html', chambers=chambers, info=info, tests=test_slot, statuses=statuses, info_versions=info_versions, logops=logops, block_title=block_title)
        # return render_template('home.html', info=info, tests=test_slot, statuses=statuses, logops=logops)


@app.route('/status/')
def status():
    return redirect('/')


@app.route('/newstatus/<string:slot_no>/')
def view_status_new(slot_no):
    setting = get_setting_by_name('chassis_name')
    if(setting):
        chassis_name = setting['value']
    else:
        chassis_name = ''
    info = {'result': "Testing", 'slot_no': slot_no,
            'chassis_name': chassis_name}
    return render_template('status_new.html', info=info)


# Create a URL route in our application for "/"
@app.route('/status/<string:slot_no>/<string:slot>/')
def view_status(slot_no=None, slot=None):
    raw_statuses = get_status_by_slot(slot_no)
    setting = get_setting_by_name('chassis_name')
    interval_setting = get_setting_by_name('interval')  
    test_slot = get_test_by_slot(slot_no)
    testcaselist = get_testcaselist_by_slot(slot_no)
    path_to_test_suite = test_slot['robot_name']

    num_list = len(testcaselist)
    if num_list <= 0:
        suite = TestData(parent=None, source=path_to_test_suite)
        num_list = len(suite.testcase_table)
        for testcase in suite.testcase_table:
            testcaselist.append(testcase.name)

    settings_info = dict()
    settings = get_settings(100)
    for item in settings:
        if item["name"] == 'product_name':
            settings_info['product_name'] = item["value"]
        elif item["name"] == 'station':
            settings_info['station'] = item["value"]
        elif item["name"] == 'slot':
            settings_info['slot'] = int(item["value"])
        elif item["name"] == 'model_test':
            settings_info['model_test'] = item["value"]

    block_title = '{}_{}'.format(
        settings_info['product_name'], settings_info['station'])

    model = settings_info['model_test']

    if(setting):
        chassis_name = setting['value']
    else:
        chassis_name = ''
    if(interval_setting):
        interval = int(interval_setting['value'])
    else:
        interval = 60
    statuses = list()
    info = {'result': "testing", 'slot_no': slot_no,
            'chassis_name': chassis_name, 'interval': interval}
    if len(raw_statuses) == 0:
        abort(404)
    for index, item in enumerate(raw_statuses):
        if item["status"] == 'start_test':
            elapsed_time = datetime.datetime.now() - item['created']
            statuses.append({'name': item['message'], 'status': 'testing', 'started': item['created'],
                             'finished': None, 'elapsed_time': str(elapsed_time).split('.')[0], 'reason': ''})
        elif item["status"] == 'end_test':
            msg = item['message'].split(' ', 1)
            statuses[-1]['status'] = msg[0].replace("Result:", "")
            if statuses[-1]['status'] == "PASS":
                statuses[-1]['status'] = "passes"
            elif statuses[-1]['status'] == "ABORT":
                statuses[-1]['status'] = "aborted"
            else:
                statuses[-1]['status'] = "failed"

            if len(msg) > 1:
                statuses[-1]['reason'] = msg[1]
            else:
                statuses[-1]['reason'] = '-'
            statuses[-1]['finished'] = item['created']
            elapsed_time = statuses[-1]['finished'] - statuses[-1]['started']
            statuses[-1]['elapsed_time'] = str(elapsed_time).split('.')[0]
        elif item["status"] == 'end_suite':
            info["result"] = statuses[-1]['status']
        else:
            print(index, item)

    num_diff = num_list - (len(raw_statuses) / 2)
    for testcase in testcaselist:
        if num_list <= num_diff:
            statuses.append({'name': testcase, 'status': 'Wait', 'started': None,
                             'finished': None, 'elapsed_time': '', 'reason': ''})
        num_list -= 1

    release_version = get_release_version_by_location(slot)

    info["code_version"] = release_version['value']
    info["logop"] = test_slot['logop']
    info["test_mode"] = test_slot['test_mode']
    info["slot_no"] = int(info["slot_no"])
    if info["logop"] == "chamber":
        info["slot_no"] = info["slot_no"] - settings_info['slot']

    print('info : {}'.format(info))

    return render_template('status.html', statuses=statuses, info=info, model=model, block_title=block_title)


@app.route('/status/<string:slot_no>/<string:slot>/view/<string:filename>')
def show_status_log(slot_no=None, slot=None, filename=None):
    settings_info = dict()
    settings = get_settings(100)
    for item in settings:
        if item["name"] == 'product_name':
            settings_info['product_name'] = item["value"]
        elif item["name"] == 'station':
            settings_info['station'] = item["value"]

    block_title = '{}_{}'.format(
        settings_info['product_name'], settings_info['station'])

    name = get_setting_by_name('chassis_name')
    info = dict()
    info['chassis_name'] = name['value']
    raw_logs = view_status_rawlog(slot_no, slot, filename, info)
    sequence_logs = view_status_sequencelog(slot_no, slot, filename, info)
    # print(data)
    return render_template('view_log.html', raw_logs=raw_logs, sequence_logs=sequence_logs, filename=filename, block_title=block_title)


@app.route('/userinteraction/<string:slot_no>/')
def view_user_interaction(slot_no):
    settings_info = dict()
    settings = get_settings(100)
    for item in settings:
        if item["name"] == 'product_name':
            settings_info['product_name'] = item["value"]
        elif item["name"] == 'station':
            settings_info['station'] = item["value"]

    block_title = '{}_{}'.format(
        settings_info['product_name'], settings_info['station'])

    interaction = get_interaction_by_slot(slot_no)
    if not interaction:
        abort(404)
    name = get_setting_by_name('chassis_name')
    info = dict()
    info['chassis_name'] = name['value']
    info['slot_no'] = slot_no
    test_slot = get_test_by_slot(slot_no)
    info['test_mode'] = test_slot["test_mode"]
    html = interaction['html']

    slot = info["chassis_name"] + slot_no
    testing_model = Testing()
    testing_model.root_path = info['test_mode'], slot
    filepath = testing_model.getInteractionimagesPath
    filepath = filepath[1:]

    return render_template(html, interaction=interaction, filepath=filepath, info=info, block_title=block_title)


@app.route('/userinteraction/<string:slot_no>/', methods=['POST'])
def submit_answer(slot_no):
    data = request.form.to_dict()
    print(data)
    interaction = get_interaction(int(data['id']))
    interaction['answer'] = data['answer']
    interaction['operation_id'] = data['operation_id']
    if data.get('reason'):
        interaction['reason'] = data['reason']
    else:
        interaction['reason'] = '-'
    print(interaction)
    put_interaction(interaction)
    return redirect('/')

# Create a URL route in our application for "/"
@app.route('/setting')
def setting():
    """
    This function just responds to the browser ULR
    localhost:5000/
    :return:        the rendered template 'home.html'
    """
    settings_info = dict()
    settings = get_settings(100)
    for item in settings:
        if item["name"] == 'product_name':
            settings_info['product_name'] = item["value"]
        elif item["name"] == 'station':
            settings_info['station'] = item["value"]

    block_title = '{}_{}'.format(
        settings_info['product_name'], settings_info['station'])

    return render_template('setting.html', settings=settings, block_title=block_title)
    # return render_template('setting.html', settings=settings)

# Create a URL route in our application for "/"
@app.route('/setting/add/')
def add_setting(form_data=None):
    if form_data:
        data = form_data
    else:
        data = {}

    setting = Setting()

    settings_info = dict()
    settings = get_settings(100)
    for item in settings:
        if item["name"] == 'product_name':
            settings_info['product_name'] = item["value"]
        elif item["name"] == 'station':
            settings_info['station'] = item["value"]

    block_title = '{}_{}'.format(
        settings_info['product_name'], settings_info['station'])

    return render_template('setting_add.html', form_data=data, block_title=block_title)


@app.route('/setting/add/', methods=['POST'])
def submit_add_setting():
    data = request.form.to_dict()

    test = get_setting_by_name(data["name"])
    print(test)
    if test != ('Not found', 404):
        flash('Duplicate setting name', 'danger')
        return render_template('setting_add.html', form_data=data)
    setting = {"id": None, "name": data["name"], "title": data["title"],
               "value": data["value"], "categories": data["categories"], "order": int(data["order"])}
    put_setting(setting)
    flash('You were successfully save settings', 'success')
    return redirect(url_for('setting'))


@app.route('/logop/add/')
def add_logop(form_data=None):
    if form_data:
        data = form_data
    else:
        data = {}

    settings_info = dict()
    settings = get_settings(100)
    for item in settings:
        if item["name"] == 'product_name':
            settings_info['product_name'] = item["value"]
        elif item["name"] == 'station':
            settings_info['station'] = item["value"]

    block_title = '{}_{}'.format(
        settings_info['product_name'], settings_info['station'])

    return render_template('logop_add.html', form_data=data, block_title=block_title)


@app.route('/logop/add/', methods=['POST'])
def submit_add_logop():
    data = request.form.to_dict()

    logop = {"id": None, "name": data["name"], "order": int(data["order"])}
    put_logop(logop)

    # get old data json logop
    with open(logop_json_path) as json_file:
        logop_json_decoded = json.load(json_file)

    # set new data json logop
    logop_json_decoded[data["name"]] = {'order': int(data["order"])}

    # Update data json logop file
    with open(logop_json_path, 'w') as outfile:
        json.dump(logop_json_decoded, outfile)

    flash('You were successfully save logop', 'success')
    return redirect(url_for('setting'))


@app.route('/logop/remove/')
def remove_logop():
    settings_info = dict()
    settings = get_settings(100)
    for item in settings:
        if item["name"] == 'product_name':
            settings_info['product_name'] = item["value"]
        elif item["name"] == 'station':
            settings_info['station'] = item["value"]

    block_title = '{}_{}'.format(
        settings_info['product_name'], settings_info['station'])

    logops = get_logop(100)

    return render_template('logop_remove.html', logops=logops, block_title=block_title)


@app.route('/logop/remove/', methods=['POST'])
def submit_remove_logop():
    data = request.form.to_dict()
    delete_logop(data["logop"])

    # get old data json logop
    with open(logop_json_path) as json_file:
        logop_json_decoded = json.load(json_file)

    # set new data json logop
    logop_json_decoded.pop(data["logop"])

    # Update data json logop file
    with open(logop_json_path, 'w') as outfile:
        json.dump(logop_json_decoded, outfile)

    flash('You were successfully save logop', 'success')
    return redirect(url_for('setting'))


@app.route('/setting', methods=['POST'])
def save_setting():
    data = request.form.to_dict()

    info = dict()
    settings = get_settings(100)
    for item in settings:
        if item["name"] == 'slot':
            info['slot'] = int(item["value"])
        elif item["name"] == 'model_test':
            info['model_test'] = item["value"]

    """
    This function just responds to the browser ULR
    localhost:5000/
    :return:        the rendered template 'home.html'
    """
    tests = get_tests(100)
    if len(tests) > 0:
        flash('please clear all tests before save setting', 'danger')
        return redirect(url_for('setting'))

    print('setting_POST', type(data))

    slot = json.dumps(int(data["slot"]))
    chassis_name = json.dumps(data["chassis_name"])
    chamber = json.dumps(int(data["chamber"]))

    model_test = json.dumps(data["model_test"])

    # num_slot = int(float(slot))
    print(int(slot))
    print(type(int(slot)))
    print(int(chamber))

    chassis = chassis_name.strip('"\"')
    print(chassis)
    model = model_test.strip('"\"')

    print("uuuuu"+model)

    if model == "sub-slot":

        print("SubSlotacsaca")

        print("test_slot")

        # data_value = '{"release_path_version":"empty"}'

        with open(release_version_json_path) as json_file:
            # with open("/opt/Robot/release_version.json", "w") as file:

            json_decoded = json.load(json_file)
            # print(json_decoded)
            slot_status = []

            for i in json_decoded:
                # slot_status.append(json_decoded[i]["release_path_version"])

                # if slot_status != "empty":
                #     print(slot_status)
                #     flash('please clear zoned', 'danger')
                #     return redirect(url_for('setting'))

                slot_status.append(json_decoded[i]["release_path_version"])

                # print(slot_status)

                if json_decoded[i]["release_path_version"] != "empty":
                    print(slot_status)
                    flash('please clear zoned', 'danger')

                    return redirect(url_for('setting'))

            with open(release_version_json_path, "w") as file:

                constJSONstr = {}
                str_json = {"release_path_version": "empty"}
                x = 1
                # for i in range(len(chassis_name)):
                while x != int(slot)+1:
                    print("i", x)
                    constJSONstr[chassis+str(x)] = str_json
                    constJSONstr[chassis+str(x)+"_1"] = str_json
                    constJSONstr[chassis+str(x)+"_2"] = str_json
                    constJSONstr[chassis+str(x)+"_3"] = str_json
                    constJSONstr[chassis+str(x)+"_4"] = str_json
                    # constJSON.append({chassis+str(x):{"release_path_version":"empty"}})

                    x += 1
                print("json", constJSONstr)

                chamberJSONstr = {}
                y = 1
                # for i in range(len(chassis_name)):
                while y != int(chamber)+1:
                    print("y", y)
                    print(type(y))
                    print(type(slot))
                    num_chamber = y+int(slot)
                    chamberJSONstr['chamber'+str(num_chamber)] = str_json

                    # constJSON.append({chassis+str(x):{"release_path_version":"empty"}})

                    y += 1
                print("chamberJSONstr", chamberJSONstr)

                dist_json = dict(constJSONstr)
                dist_json.update(chamberJSONstr)
                print("json_fianl", dist_json)

                json.dump(dist_json, file)
        # os.system(
        #     'ln -s /opt/Robot/release_version.json webapps/static/js/release_version.json')

        # get old data json setting
        with open(setting_json_path) as json_file:
            setting_json_decoded = json.load(json_file)

        # set new data json setting
        for item in data:
            setting_json_decoded[item]['value'] = data[item]

        # Update data json setting file
        with open(setting_json_path, 'w') as outfile:
            json.dump(setting_json_decoded, outfile)

        save_all_setting(data)
        flash('You were successfully save settings', 'success')

        time.sleep(3)

    else:

        with open(release_version_json_path) as json_file:
            # with open("/opt/Robot/release_version.json", "w") as file:

            json_decoded = json.load(json_file)
            print(json_decoded)
            slot_status = []

            for i in json_decoded:
                # slot_status.append(json_decoded[i]["release_path_version"])

                # if slot_status != "empty":
                #     print(slot_status)
                #     flash('please clear zoned', 'danger')
                #     return redirect(url_for('setting'))

                slot_status.append(json_decoded[i]["release_path_version"])

                # print(slot_status)

                if json_decoded[i]["release_path_version"] != "empty":
                    print(slot_status)
                    flash('please clear zoned', 'danger')

                    return redirect(url_for('setting'))

            with open(release_version_json_path, "w") as file:

                constJSONstr = {}
                str_json = {"release_path_version": "empty"}
                x = 1
                # for i in range(len(chassis_name)):
                while x != int(slot)+1:
                    print("i", x)
                    constJSONstr[chassis+str(x)] = str_json
                    # constJSON.append({chassis+str(x):{"release_path_version":"empty"}})

                    x += 1
                print("json", constJSONstr)

                chamberJSONstr = {}
                y = 1
                # for i in range(len(chassis_name)):
                while y != int(chamber)+1:
                    print("y", y)
                    print(type(y))
                    print(type(slot))
                    num_chamber = y + int(slot)
                    chamberJSONstr['chamber'+str(num_chamber)] = str_json

                    # constJSON.append({chassis+str(x):{"release_path_version":"empty"}})

                    y += 1
                print("chamberJSONstr", chamberJSONstr)

                dist_json = dict(constJSONstr)
                dist_json.update(chamberJSONstr)
                print("json_fianl", dist_json)

                json.dump(dist_json, file)

                for idx, val in enumerate(dist_json):
                    print(idx, val)

                    code_version = {"id": None, "location": val, "value": "empty"}
                    put_release_version(code_version)

        # os.system('ln -s /opt/Robot/release_version.json webapps/static/js/release_version.json')

        # get old data json setting
        with open(setting_json_path) as json_file:
            setting_json_decoded = json.load(json_file)

        # set new data json setting
        for item in data:
            setting_json_decoded[item]['value'] = data[item]

        # Update data json setting file
        with open(setting_json_path, 'w') as outfile:
            json.dump(setting_json_decoded, outfile)

        save_all_setting(data)
        flash('You were successfully save settings', 'success')

        time.sleep(3)

    return redirect(url_for('setting'))

# Add Distibution Setting
@app.route('/setting/distribution/')
def setting_distribution(form_data=None):
    if form_data:
        data = form_data
    else:
        data = {}

    settings_info = dict()
    settings = get_settings(100)
    for item in settings:
        if item["name"] == 'product_name':
            settings_info['product_name'] = item["value"]
        elif item["name"] == 'station':
            settings_info['station'] = item["value"]

    block_title = '{}_{}'.format(
        settings_info['product_name'], settings_info['station'])

    return render_template('setting_distribution.html', form_data=data, block_title=block_title)

# Add Distibution Home
@app.route('/distribution/home/')
def distribution_home(form_data=None):
    if form_data:
        data = form_data
    else:
        data = {}

    info = dict()
    settings = get_settings(100)
    for item in settings:
        if item["name"] == 'station':
            info['station'] = item["value"]
        elif item["name"] == 'product_name':
            info['product_name'] = item["value"]
        elif item["name"] == 'station':
            info['station'] = item["value"]

    block_title = '{}_{}'.format(info['product_name'], info['station'])

    print(info['station'])

    with open(release_version_json_path) as json_file:
        # with open('/opt/Robot/release_version.json') as json_file:
        json_decoded = json.load(json_file)
        # print(json_decoded)

        slot = []
        slot_status = []

        for i in json_decoded:
            slot.append(i)

            slot_status.append(json_decoded[i]["release_path_version"])

        # print(slot)
        # print(slot_status)

    return render_template('distribution_home.html', form_data=data, slot=slot, slot_status=slot_status, station=info['station'], len1=len(slot), len2=len(slot_status), block_title=block_title)

# Add Distibution Put Release
@app.route('/distribution/put_release/', methods=['GET'])
def distribution_put_release(form_data=None):
    if form_data:
        data = form_data
    else:
        data = {}

    # private token or personal token authentication
    gl = gitlab.Gitlab('http://10.196.66.66/git/',
                       private_token='449KCc3c_snVhFX16m8f', per_page=100)
    # gl = gitlab.Gitlab('http://110.164.64.68/',email='pkhanma@celestica.com',password='thesis767Tee',api_version=4)

    gl.auth()

    datagroup = []
    group = gl.groups.list(all=True)
    for groups in group:
        # print(project.id[536])
        print(groups.name)

        item = groups.name
        datagroup.append(item)

    settings_info = dict()
    settings = get_settings(100)
    for item in settings:
        if item["name"] == 'product_name':
            settings_info['product_name'] = item["value"]
        elif item["name"] == 'station':
            settings_info['station'] = item["value"]

    block_title = '{}_{}'.format(
        settings_info['product_name'], settings_info['station'])

    return render_template('distribution_put_release.html', datagroup=datagroup, len3=len(datagroup), block_title=block_title)


@app.route('/distribution/put_release/', methods=['POST'])
def submit_put_release(form_data=None):
    if form_data:
        data = form_data
    else:
        data = {}

    print("yyyy")

    # private token or personal token authentication
    gl = gitlab.Gitlab('http://10.196.66.66/git/',
                       private_token='449KCc3c_snVhFX16m8f', per_page=100)
    # gl = gitlab.Gitlab('http://110.164.64.68/',email='pkhanma@celestica.com',password='thesis767Tee',api_version=4)BSM_EEPROM_TOOLS

    gl.auth()

    user = "robot"
    password = "Robot123"

    repo = (str(request.form.get('repo_select')))
    tag = (str(request.form.get('tag')))
    group = (str(request.form.get('group')))

    print(repo)
    print(tag)
    print(group)

    # isDirectory = os.path.isdir(repo)
    # print(isDirectory, "isDirectory")

    # if isDirectory == False:
    #     path = os.path.join('.', repo)
    #     os.mkdir(path)
    #     print("Directory '% s' created" % repo)

    projects = gl.projects.list()
    for project in projects:
        print(project.name)

        # id_project = project.id
        if project.name == repo:
            id_project = project.id
            # project = gl.projects.create(data)
            project = gl.projects.get(id_project)
            # project = gl.projects.get(513)
            # print(project.attributes)  # displays all the attributes
            # git_url = "http://203.170.244.69/git/Robot-Framework/Wedge400-Project/wedge400-c_bi_rdt_ess_stations./"
            # subprocess.call(['git', 'clone','--depth 1','--branch','Wedge400_2020.07.29-01', git_url])
            tags_list = project.tags.list()
            for tag_name in tags_list:

                # print("tag pick",tag)
                if tag == tag_name.name:

                    web_url = json.dumps(tag_name.commit["web_url"])
                    print("URL", web_url)
                    # print("sha", json.dumps(tag_name.commit["short_id"]))
                    sha_str = json.dumps(tag_name.commit["short_id"])
                    sha_id = sha_str.strip('"\"')
                    print("sha..", sha_id)
                    print("id_project", id_project)
                    # parent_ids = json.dumps(tag_name.commit["parent_ids"])
                    # print("parent_ids", parent_ids)

                    str_url = web_url.split("/")
                    print("str_path1", str_url[4])
                    print("str_path2", str_url[5])
                    print("str_path3", str_url[6])

                    parent_ids = str_url[9].rstrip('"')
                    print("parent_ids", parent_ids)

                    # url = 'git clone --depth 1 --branch {0} http://{1}:{2}@203.170.244.69/git/Robot-Framework/Minipack2-Project/{3}/'.format(tag,user,password,repo)
                    # url = 'git clone --depth 1 --branch {0} http://{1}:{2}@10.196.66.66/git/{3}/{4}/{5}/'.format(
                    # tag, user, password, str_url[4], str_url[5], repo)
                    # url = 'git clone --depth 1 --branch Wedge400_2020.07.29-01 http://pkhanma:thesis767Tee@203.170.244.69/git/Robot-Framework/Wedge400-Project/Wedge400-C_BI_RDT_ESS_Stations./'
                    url = 'wget -continue --header "PRIVATE-TOKEN: 449KCc3c_snVhFX16m8f" "http://10.196.66.66/git/api/v4/projects/{}/repository/archive.tar.gz?sha={}" -O {}/{}.tar.gz'.format(
                        id_project, sha_id, dir_path, tag)
                #     url = 'wget -O firmware_config.json --header "PRIVATE-TOKEN: 449KCc3c_snVhFX16m8f" "http://10.196.66.66/git/api/v4/projects/{0}/repository/files/Package%2ffirmware_config.json/raw?ref={1}" '.format(
                # id_project, tag_global)

                    proc = subprocess.Popen(
                        url, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    # time.sleep(120)

                    while proc.poll() is None:
                        result = proc.stdout.read()

                        print("taggggg", type(tag))
                        print(repo)

                        tar = tarfile.open(dir_path+'/'+tag+'.tar.gz')
                        # specify which folder to extract to
                        tar.extractall(dir_path)
                        tar.close()

                        with tarfile.open('{}/{}.tar.gz'.format(dir_path, tag), "w:gz") as tar:
                            tar.add(dir_path+'/'+'{}-{}-{}'.format(
                                str_url[6], sha_id, parent_ids), arcname=os.path.basename(tag))

                        print('{}.tar.gz'.format(tag), "send name")
                        send_name = '{}.tar.gz'.format(tag)

                        ssh_client = paramiko.SSHClient()
                        ssh_client.set_missing_host_key_policy(
                            paramiko.AutoAddPolicy())
                        ssh_client.connect(hostname="10.196.66.71", username="disserver",
                                           password="tde123Admin")
                        ftp = ssh_client.open_sftp()

                        # files = glob(send_name)
                        # print("files", files)

                        file_path = dir_path+'/'+send_name
                        destination_path = dist_release_path+send_name

                        print("file_path", file_path)

                        sftp = ssh_client.open_sftp()
                        sftp.put(file_path, destination_path)
                        sftp.close()
                        ssh_client.close()

                    folder = dir_path+'/'+str_url[6]+'-'+sha_id+'-'+parent_ids
                    print("file_path", repo)
                    os.system('pwd')
                    for filename in os.listdir(folder):
                        file_path = os.path.join(folder, filename)

                        try:
                            if os.path.isfile(file_path) or os.path.islink(file_path):
                                os.unlink(file_path)
                            elif os.path.isdir(file_path):
                                shutil.rmtree(file_path)
                        except Exception as e:
                            print('Failed to delete %s. Reason: %s' %
                                  (file_path, e))
                    os.rmdir(folder)
                    os.remove(dir_path+'/'+send_name)

        info = dict()
        settings = get_settings(100)
        for item in settings:
            if item["name"] == 'station':
                info['station'] = item["value"]
            if item["name"] == 'product_name':
                info['product_name'] = item["value"]

        block_title = '{}_{}'.format(info['product_name'], info['station'])

        # print(info['station'])

        with open(release_version_json_path) as json_file:
            # with open('/opt/Robot/release_version.json') as json_file:
            json_decoded = json.load(json_file)
            # print(json_decoded)

            slot = []
            slot_status = []

            for i in json_decoded:
                slot.append(i)

                slot_status.append(json_decoded[i]["release_path_version"])

    return render_template('distribution_home.html', slot=slot, slot_status=slot_status, station=info['station'], len1=len(slot), len2=len(slot_status), block_title=block_title)


@app.route('/get_repository/')
def get_repository():

    repo_select = request.args.get('proglang', 0, type=str)
    print("test", repo_select)

    datatag = []
    gl = gitlab.Gitlab('http://10.196.66.66/git/',
                       private_token='449KCc3c_snVhFX16m8f', per_page=100)
    gl.auth()

    datatest = []
    tags = []
    name_tag = []
    datatag = []

    projects = gl.projects.list()
    for project in projects:
        # print(project.name)

        item = project.name
        datatest.append(item)

        if project.name == repo_select:
            tags = project.tags.list()
            print(tags)
            # print(len(tags))

            for tag_name in tags:
                # name_tag = tag_name.name.list()
                # print(tag_name)

                datatag.append(tag_name.name)

    print(datatag)
    print(len(datatag))

    return render_template('distribution_tag.html', len2=len(datatag), datatag=datatag)


@app.route('/get_group/')
def get_group():

    group_select = request.args.get('proglang', 0, type=str)
    print("test_group", group_select)

    gl = gitlab.Gitlab('http://10.196.66.66/git/',
                       private_token='449KCc3c_snVhFX16m8f', per_page=100)
    gl.auth()

    tags = []
    dataproject = []

    group = gl.groups.list(all=True)

    # first_group_project = group.projects.list()[0]
    # manageable_project = gl.projects.get(first_group_project.id, lazy=True)
    # print(manageable_project, "manageable_project")

    # datagroup = []

    for groups in group:

        # item = groups.name
        # datagroup.append(item)

        if groups.name == group_select:

            print("sub_group_id", groups.id)

            subgroups = gl.groups.get(groups.id).subgroups.list()
            # group = gl.groups.get(subgroups[3].id)
            print("sub_group", subgroups)

            # subgroups = groups.get(176).subgroups.list()

            repo = groups.projects.list()
            print(repo)

            for project in repo:
                item = project.name
                # item = project.name
                print(item)
                dataproject.append(item)

    return render_template('distribution_repo.html', len2=len(dataproject), dataproject=dataproject)

# Add Distibution Zone Release
@app.route('/distribution/zone_release/')
def distribution_zone_release(form_data=None):
    if form_data:
        data = form_data
    else:
        data = {}

    info = dict()
    settings = get_settings(100)
    for item in settings:
        if item["name"] == 'station':
            info['station'] = item["value"]
        elif item["name"] == 'slot':
            info['slot'] = int(item["value"])
        elif item["name"] == 'chassis_name':
            info['chassis_name'] = item["value"]
        elif item["name"] == 'chamber':
            info['chamber'] = int(item["value"])
        elif item["name"] == 'model_test':
            info['model_test'] = item["value"]
        if item["name"] == 'product_name':
            info['product_name'] = item["value"]

    block_title = '{}_{}'.format(info['product_name'], info['station'])

    tests = get_tests(100)
    test_slot = list()
    chambers = list()

    print("_slot", info['slot'])

    for i in range(1, info['slot']+1):
        test_slot.append(dict())
    statuses = get_statuses(100)

    print(test_slot)

    for item in tests:
        item["statuses"] = sorted(
            item["statuses"], key=lambda i: i['id'], reverse=True)
        item["test_info"] = dict()

        # if len(item["statuses"]) > 0:
        test_slot[int(item["location"])-1] = item

    for i in range(1, info['chamber']+1):
            # chambers.append(dict())
        print("chamber_slot", i + info['slot'])
        chambers.append('chamber'+str(i + info['slot']))

    if info['model_test'] == "sub-slot":

        for i in range(1, info['chamber']+1):
            # chambers.append(dict())
            print("chamber_slot", i+info['slot'])
            chambers.append('chamber'+str(i+info['slot']))

    # print("chamber_slot",type(chambers))

    # URL = "http://10.196.66.71:5000/api/zone_release"

    # res = requests.get("http://10.196.66.71:5000/api/zone_release")

    # print(res.text)
    # print(res.content)

    # data_list = list(res.text.split(","))

    # print(data_list)

    # s = socket.socket()  # create a socket object
    # host = '10.196.66.71'  # Host i.p
    # port = 12388  # Reserve a port for your service

    # s.connect((host, port))
    # # s.send('Hello server!')

    # data = (str(s.recv(1024), 'utf-8'))

    # data_list = ast.literal_eval(data)

    # print(data_list)

    # s.close
    # s.close()
    # print('connection closed')

    res = requests.get("http://10.196.66.71:5000/api/zone_release")

    print(type(res))
    print(str(res.text))
    print(res)

    data_list = json.loads(res.text)

    return render_template('distribution_zone_release.html', form_data=data, station=info['station'], tests=test_slot, info=info, package=data_list, len=len(data_list), block_title=block_title, chambers=chambers, len1=len(chambers))


@app.route('/distribution/zone_release/', methods=['POST'])
def submit_zone_release(form_data=None):
    if form_data:
        data = form_data
    else:
        data = {}

    print("POST_Zone")

    info = dict()
    settings = get_settings(100)
    for item in settings:
        if item["name"] == 'station':
            info['station'] = item["value"]
        elif item["name"] == 'product_name':
            info['product_name'] = item["value"]
        elif item["name"] == 'station':
            info['station'] = item["value"]

    block_title = '{}_{}'.format(info['product_name'], info['station'])

    station = info['station']
    filename = (str(request.form.get('package')))
    # slot = (str(request.form.get('slot')))
    slot = request.form.getlist('slot')
    print(station)
    print(filename)
    print(slot)

    info = dict()
    settings = get_settings(100)
    for item in settings:
        if item["name"] == 'slot':
            info['slot'] = int(item["value"])
        elif item["name"] == 'operation':
            info['operation'] = item["value"]
        elif item["name"] == 'chassis_name':
            info['chassis_name'] = item["value"]
        elif item["name"] == 'station':
            info['station'] = item["value"]
        elif item["name"] == 'parameter':
            info['parameter'] = item["value"]
        elif item["name"] == 'interval':
            info['interval'] = int(item["value"])
        elif item["name"] == 'log_template':
            info['log_template'] = item["value"]
        elif item["name"] == 'version':
            info['version'] = item["value"]
        elif item["name"] == 'model_test':
            info['model_test'] = item["value"]

    tests = get_tests(100)
    test_slot = list()

    test_id = 0

    for i in range(1, info['slot']+1):
        test_slot.append(dict())
    statuses = get_statuses(100)

    # print(info['chassis_name'])
    for item in tests:
        item["statuses"] = sorted(
            item["statuses"], key=lambda i: i['id'], reverse=True)
        item["test_info"] = dict()
        if len(item["statuses"]) > 0:
            # set created time from first test case created
            item["test_info"]["created"] = item["statuses"][-1]["created"]
            # remove timezone string
            if ":" == item["test_info"]["created"][-3:-2]:
                item["test_info"]["created"] = item["test_info"]["created"][:-3] + \
                    item["test_info"]["created"][-2:]
            if ":" == item["statuses"][0]["created"][-3:-2]:
                item["statuses"][0]["created"] = item["statuses"][0]["created"][:-3] + \
                    item["statuses"][0]["created"][-2:]

            # check last status not end suite(still testing)
            if item["statuses"][0]["status"] != "end_suite":
                # loop to find failing
                item["test_info"]["status"] = "Testing"
                for test_case in item["statuses"]:
                    # if end testcase  and message is fail
                    if test_case["status"] == "end_test" and test_case["message"].split(':')[1][:4] == "FAIL":
                        item["test_info"]["status"] = "failing"
                        break

                item["test_info"]["test_case"] = item["statuses"][0]["message"]
                created_time = datetime.datetime.strptime(
                    item["test_info"]["created"], "%Y-%m-%dT%H:%M:%S.%f%z")
                # get timezone info
                tz = datetime.datetime.now(
                    datetime.timezone.utc).astimezone().tzinfo
                # change time object to use same timezone and differential
                elapsed_time = datetime.datetime.now(
                    tz) - created_time.replace(tzinfo=tz)
                # remove millisecond
                item["test_info"]["elapsed_time"] = str(
                    elapsed_time).split('.')[0]
            else:
                created_time = datetime.datetime.strptime(
                    item["test_info"]["created"], "%Y-%m-%dT%H:%M:%S.%f%z")
                finished_time = datetime.datetime.strptime(
                    item["statuses"][0]["created"], "%Y-%m-%dT%H:%M:%S.%f%z")
                elapsed_time = finished_time - created_time
                item["test_info"]["elapsed_time"] = str(
                    elapsed_time).split('.')[0]
                item["test_info"]["status"] = item["statuses"][0]["message"].split(':')[
                    1].strip()

                if item["test_info"]["status"] == "FAIL":
                    length = (len(item["statuses"]))

                    # for test_case in reversed(item["statuses"]):  # loop item status to find first error message
                    for z in reversed(range(length)):
                        print(z, end=" ")
                        print(item["statuses"][z])

                        if item["statuses"][z]["status"] == "end_test" and item["statuses"][z]["message"].split(':')[1][:5] == "ABORT":
                            item["test_info"]["created"] = item["statuses"][z]["message"].split(':')[
                                1][:5]
                            print('------test_abort' +
                                  item["test_info"]["created"])
                            test_id = -1
                            break
                        elif item["statuses"][z]["status"] == "end_test" and item["statuses"][z]["message"].split(':')[1][:4] == "FAIL":
                            item["test_info"]["message"] = item["statuses"][z]["message"].replace(
                                "Result:FAIL ", "")
                            test_id = z
                            print('######test_case_fail_name######' +
                                  item["test_info"]["message"])
                            print('######test_case_fail_nameID######'+str(test_id))
                            break

                    for x in range(length):

                        print('######ID######'+str(test_id))
                        if test_id == -1:
                            print('######ABORT######'+str(test_id))

                        elif x == test_id+1:
                            # item["test_info"]["message"] = test_case["message"].replace([1][:2],"")
                            print('######ID******'+str(x))
                            item["test_info"]["test_db"] = item["statuses"][x]["message"]

                            break

                    item["test_info"]["status"] = "failed"
                elif item["test_info"]["status"] == "PASS":
                    item["test_info"]["status"] = "passes"
                else:
                    item["test_info"]["status"] = "failed"
        test_slot[int(item["location"])-1] = item
        # print("STAY", test_slot)
        for index, item in enumerate(test_slot):
            # print(index,item)
            # for val in test_slot[index]:
            location = []
            for key in item:
                value = item[key]
                # print(key, value)

                if key == "location":
                    # if value != '':
                    print(value)

                    ck_slot = slot[-1]
                    print("dan"+ck_slot)

                    if value == ck_slot:
                        print("danger")
                        flash('please clear this slot before zone release', 'danger')
                        # time.sleep(2)

                        with open(release_version_json_path) as json_file:
                            # with open('/opt/Robot/release_version.json') as json_file:
                            json_decoded = json.load(json_file)
                            print(json_decoded)

                            slot = []
                            slot_status = []

                            for i in json_decoded:
                                slot.append(i)

                                slot_status.append(
                                    json_decoded[i]["release_path_version"])

                        return render_template('distribution_home.html', form_data=data, slot=slot, slot_status=slot_status, station=station, len1=len(slot), len2=len(slot_status))

    host = '10.196.66.71'
    port = 22
    username = 'disserver'

    files = glob(filename)
    remote_images_path = dist_release_path
    local_path = robot_root_path

    print("files", files)

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(
        paramiko.AutoAddPolicy())
    ssh_client.connect(hostname="10.196.66.71", username="disserver",
                       password="tde123Admin")
    sftp = ssh_client.open_sftp()
    sftp.get(remote_images_path+filename, local_path+filename)
    sftp.close()
    ssh_client.close()

    folderdel = filename[:-7]
    if os.path.exists(local_path+folderdel):
        os.system('rm -rf '+local_path+folderdel)

    tar = tarfile.open(robot_root_path+filename)
    tar.extractall(robot_root_path)  # specify which folder to extract to
    tar.close()

    foldername = filename[:-7]
    print('tests', foldername)

    config_file = robot_root_path+foldername+'/Package/firmware_config.json'

    with open(config_file) as json_file:
        json_decoded = json.load(json_file)

        if json_decoded == {}:
            for idx, val in enumerate(slot):
                print(idx, val)
                with open(release_version_json_path) as json_file:
                    json_decoded = json.load(json_file)
                    print(json_decoded[val]["release_path_version"])

                json_decoded[val]["release_path_version"] = foldername

                with open(release_version_json_path, 'w') as json_file:
                    json.dump(json_decoded, json_file)

                code_version = {"id": None,
                                "location": val, "value": foldername}
                put_release_version(code_version)

            with open(dir_path+'/release_version.json') as json_file:
                json_decoded = json.load(json_file)
                print("empty json", json_decoded)

            with open(release_version_json_path) as json_file:
                # with open('/opt/Robot/release_version.json') as json_file:
                json_decoded = json.load(json_file)
                print(json_decoded)

                slot = []
                slot_status = []

                for i in json_decoded:
                    slot.append(i)

                    slot_status.append(
                        json_decoded[i]["release_path_version"])

            return render_template('distribution_home.html', form_data=data, slot=slot, slot_status=slot_status, station=station, len1=len(slot), len2=len(slot_status))

        # print(json_decoded)
        else:
            for (k, v) in json_decoded.items():
                print("Key: " + k)
                print("Value: " + str(v))

                for (sk, sv) in v.items():
                    print("Key1: " + sk)
                    print("Value1: " + str(sv))

                    for (skt, svt) in sv.items():
                        print("Key2: " + skt)
                        print("Value2: " + str(svt))

                        desination = svt['desination']
                        file_source = svt['file']

                        print("desination: " + svt['desination'])
                        print("file_source: " + svt['file'])

                        if "," not in file_source:
                            file_pac = file_source
                            print(type(file_source))
                            if not os.path.exists(robot_root_path+k+'/Package'):
                                print("55")
                                os.makedirs(robot_root_path+k+'/Package')

                            if not os.path.exists(robot_root_path+k+'/Package/Products'):
                                print("66")
                                os.makedirs(robot_root_path+k +
                                            '/Package/Products')

                            sub_path = svt['desination'].split("/")
                            print(sub_path)
                            print(len(sub_path))

                            if len(sub_path) == 5:
                                if not os.path.exists(robot_root_path+k+'/Package/Products/'+sk):
                                    print("77")
                                    os.makedirs(robot_root_path+k +
                                                '/Package/Products/'+sk)

                                if not os.path.exists(robot_root_path+k+'/Package/Products/'+sk+'/'+sub_path[1]):
                                    print("88")
                                    os.makedirs(
                                        robot_root_path+k+'/Package/Products/'+sk+'/'+sub_path[1])

                                if not os.path.exists(robot_root_path+k+'/Package/Products/'+sk+'/'+sub_path[1]+'/'+sub_path[2]):
                                    print("99")
                                    os.makedirs(
                                        robot_root_path+k+'/Package/Products/'+sk+'/'+sub_path[1]+'/'+sub_path[2])

                                if not os.path.exists(robot_root_path+k+'/Package/Products/'+sk+'/'+sub_path[1]+'/'+sub_path[2]+'/'+sub_path[3]):
                                    print("00")
                                    os.makedirs(robot_root_path+k+'/Package/Products/' +
                                                sk+'/'+sub_path[1]+'/'+sub_path[2]+'/'+sub_path[3])

                            if len(sub_path) == 4:
                                if not os.path.exists(robot_root_path+k+'/Package/Products/'+sk):
                                    print("77")
                                    os.makedirs(robot_root_path+k +
                                                '/Package/Products/'+sk)

                                if not os.path.exists(robot_root_path+k+'/Package/Products/'+sk+'/'+sub_path[1]):
                                    print("88")
                                    os.makedirs(
                                        robot_root_path+k+'/Package/Products/'+sk+'/'+sub_path[1])

                                if not os.path.exists(robot_root_path+k+'/Package/Products/'+sk+'/'+sub_path[1]+'/'+sub_path[2]):
                                    print("99")
                                    os.makedirs(
                                        robot_root_path+k+'/Package/Products/'+sk+'/'+sub_path[1]+'/'+sub_path[2])

                            if len(sub_path) == 3:
                                print("333"+robot_root_path +
                                      k+'/Package/Products/'+sk)
                                if not os.path.exists(robot_root_path+k+'/Package/Products/'+sk):
                                    os.makedirs(robot_root_path+k +
                                                '/Package/Products/'+sk)

                                if not os.path.exists(robot_root_path+k+'/Package/Products/'+sk+'/'+sub_path[1]):
                                    print("88")
                                    os.makedirs(
                                        robot_root_path+k+'/Package/Products/'+sk+'/'+sub_path[1])

                            remote_images_path = '/home/export/resource/'+sk+desination

                            local_path = robot_root_path+k+'/Package/Products/'+sk+desination

                            print("remote_images_pathss" +
                                  '/home/export/resource/'+sk+desination+file_pac)
                            print("local_path"+robot_root_path+k +
                                  '/Package/Products'+sk+desination+file_pac)

                            ssh_client = paramiko.SSHClient()
                            ssh_client.set_missing_host_key_policy(
                                paramiko.AutoAddPolicy())
                            ssh_client.connect(hostname="10.196.66.71", username="disserver",
                                               password="tde123Admin")
                            sftp = ssh_client.open_sftp()

                            try:

                                sftp.get(remote_images_path+file_pac,
                                         local_path+file_pac)
                            except:
                                print("e.errno")
                                flash('No have '+file_pac+' in '+desination +
                                      ', Please upload file before', 'danger')

                                with open(release_version_json_path) as json_file:
                                    # with open('/opt/Robot/release_version.json') as json_file:
                                    json_decoded = json.load(json_file)
                                    print(json_decoded)

                                    slot = []
                                    slot_status = []

                                    for i in json_decoded:
                                        slot.append(i)

                                        slot_status.append(
                                            json_decoded[i]["release_path_version"])

                                return render_template('distribution_home.html', form_data=data, slot=slot, slot_status=slot_status, station=station, len1=len(slot), len2=len(slot_status))

                            sftp.close()
                            ssh_client.close()

                        else:
                            file_source = svt['file'].split(",")
                            print(file_source)

                            for idx, item in enumerate(file_source):
                                print(item)

                                if not os.path.exists(robot_root_path+k+'/Package'):
                                    print("55")
                                    os.makedirs(robot_root_path+k+'/Package')

                                if not os.path.exists(robot_root_path+k+'/Package/Products'):
                                    print("66")
                                    os.makedirs(robot_root_path +
                                                k+'/Package/Products')

                                sub_path = svt['desination'].split("/")
                                print(sub_path)
                                print(len(sub_path))

                                if len(sub_path) == 5:
                                    if not os.path.exists(robot_root_path+k+'/Package/Products/'+sk):
                                        print("77")
                                        os.makedirs(robot_root_path+k +
                                                    '/Package/Products/'+sk)

                                    if not os.path.exists(robot_root_path+k+'/Package/Products/'+sk+'/'+sub_path[1]):
                                        print("88")
                                        os.makedirs(
                                            robot_root_path+k+'/Package/Products/'+sk+'/'+sub_path[1])

                                    if not os.path.exists(robot_root_path+k+'/Package/Products/'+sk+'/'+sub_path[1]+'/'+sub_path[2]):
                                        print("99")
                                        os.makedirs(
                                            robot_root_path+k+'/Package/Products/'+sk+'/'+sub_path[1]+'/'+sub_path[2])

                                    if not os.path.exists(robot_root_path+k+'/Package/Products/'+sk+'/'+sub_path[1]+'/'+sub_path[2]+'/'+sub_path[3]):
                                        print("00")
                                        os.makedirs(robot_root_path+k+'/Package/Products/' +
                                                    sk+'/'+sub_path[1]+'/'+sub_path[2]+'/'+sub_path[3])

                                if len(sub_path) == 4:
                                    if not os.path.exists(robot_root_path+k+'/Package/Products/'+sk):
                                        print("77")
                                        os.makedirs(robot_root_path+k +
                                                    '/Package/Products/'+sk)

                                    if not os.path.exists(robot_root_path+k+'/Package/Products/'+sk+'/'+sub_path[1]):
                                        print("88")
                                        os.makedirs(
                                            robot_root_path+k+'/Package/Products/'+sk+'/'+sub_path[1])

                                    if not os.path.exists(robot_root_path+k+'/Package/Products/'+sk+'/'+sub_path[1]+'/'+sub_path[2]):
                                        print("99")
                                        os.makedirs(
                                            robot_root_path+k+'/Package/Products/'+sk+'/'+sub_path[1]+'/'+sub_path[2])

                                if len(sub_path) == 3:
                                    print("333"+robot_root_path+k +
                                          '/Package/Products/'+sk+'/'+sub_path[1])
                                    if not os.path.exists(robot_root_path+k+'/Package/Products/'+sk+'/'+sub_path[1]):
                                        os.makedirs(robot_root_path+k +
                                                    '/Package/Products/'+sk+'/'+sub_path[1])

                                    if not os.path.exists(robot_root_path+k+'/Package/Products/'+sk+'/'+sub_path[1]):
                                        print("88")
                                        os.makedirs(
                                            robot_root_path+k+'/Package/Products/'+sk+'/'+sub_path[1])

                                remote_images_path = '/home/export/resource/'+sk+desination
                                local_path = robot_root_path+k+'/Package/Products/'+sk+desination

                                ssh_client = paramiko.SSHClient()
                                ssh_client.set_missing_host_key_policy(
                                    paramiko.AutoAddPolicy())
                                ssh_client.connect(hostname="10.196.66.71", username="disserver",
                                                   password="tde123Admin")
                                sftp = ssh_client.open_sftp()

                                try:

                                    sftp.get(remote_images_path +
                                             item, local_path+item)
                                except:
                                    print("e.errno")
                                    flash('No have '+item+' in '+sk+'/'+sub_path[1] +
                                          ', Please upload file before', 'danger')

                                    with open(release_version_json_path) as json_file:
                                        json_decoded = json.load(json_file)
                                        print(json_decoded)

                                        slot = []
                                        slot_status = []

                                        for i in json_decoded:
                                            slot.append(i)

                                            slot_status.append(
                                                json_decoded[i]["release_path_version"])

                                    return render_template('distribution_home.html', form_data=data, slot=slot, slot_status=slot_status, station=station, len1=len(slot), len2=len(slot_status))

                                sftp.close()
                                ssh_client.close()

    if info['model_test'] == "sub-slot":

        print("SubSlot")

        for idx, val in enumerate(slot):

            if val[:7] == 'chamber':
                print(val)
                print('chamber')
                with open(release_version_json_path) as json_file:
                    # with open('/opt/Robot/release_version.json') as json_file:
                    json_decoded = json.load(json_file)
                    print(json_decoded[val]["release_path_version"])

                json_decoded[val]["release_path_version"] = foldername

                with open(release_version_json_path, 'w') as json_file:
                    # with open('/opt/Robot/release_version.json', 'w') as json_file:
                    json.dump(json_decoded, json_file)

            else:
                print(val)
                print('slot')
                with open(release_version_json_path) as json_file:
                    # with open('/opt/Robot/release_version.json') as json_file:
                    json_decoded = json.load(json_file)
                    print(json_decoded[val]["release_path_version"])

                json_decoded[val]["release_path_version"] = foldername
                json_decoded[val+"_1"]["release_path_version"] = foldername
                json_decoded[val+"_2"]["release_path_version"] = foldername
                json_decoded[val+"_3"]["release_path_version"] = foldername
                json_decoded[val+"_4"]["release_path_version"] = foldername

                with open(release_version_json_path, 'w') as json_file:
                    # with open('/opt/Robot/release_version.json', 'w') as json_file:
                    json.dump(json_decoded, json_file)
    else:

        for idx, val in enumerate(slot):

            with open(release_version_json_path) as json_file:
                # with open('/opt/Robot/release_version.json') as json_file:
                json_decoded = json.load(json_file)
                print(json_decoded[val]["release_path_version"])

            json_decoded[val]["release_path_version"] = foldername

            with open(release_version_json_path, 'w') as json_file:
                # with open('/opt/Robot/release_version.json', 'w') as json_file:
                json.dump(json_decoded, json_file)

            code_version = {"id": None, "location": val, "value": foldername}
            put_release_version(code_version)

    with open(release_version_json_path) as json_file:
        # with open('/opt/Robot/release_version.json') as json_file:
        json_decoded = json.load(json_file)
        print(json_decoded)

        slot = []
        slot_status = []

        for i in json_decoded:
            slot.append(i)

            slot_status.append(json_decoded[i]["release_path_version"])

    return render_template('distribution_home.html', form_data=data, slot=slot, slot_status=slot_status, station=station, len1=len(slot), len2=len(slot_status))

# Add Distibution Zone Release
@app.route('/distribution/purge_release/')
def distribution_purge_release(form_data=None):
    if form_data:
        data = form_data
    else:
        data = {}

    info = dict()
    settings = get_settings(100)
    for item in settings:
        if item["name"] == 'station':
            info['station'] = item["value"]
        elif item["name"] == 'slot':
            info['slot'] = int(item["value"])
        elif item["name"] == 'chassis_name':
            info['chassis_name'] = item["value"]
        elif item["name"] == 'chamber':
            info['chamber'] = int(item["value"])
        elif item["name"] == 'model_test':
            info['model_test'] = item["value"]

    tests = get_tests(100)
    test_slot = list()
    chambers = list()

    for i in range(1, info['slot']+1):
        test_slot.append(dict())
    statuses = get_statuses(100)

    for item in tests:
        item["statuses"] = sorted(
            item["statuses"], key=lambda i: i['id'], reverse=True)
        item["test_info"] = dict()

        # if len(item["statuses"]) > 0:
        test_slot[int(item["location"])-1] = item

    for i in range(1, info['chamber']+1):
            # chambers.append(dict())
        print("chamber_slot", i + info['slot'])
        chambers.append('chamber'+str(i + info['slot']))

    if info['model_test'] == "sub-slot":

        for i in range(1, info['chamber']+1):
            # chambers.append(dict())
            print("chamber_slot", i+info['slot'])
            chambers.append('chamber'+str(i+info['slot']))

    print("chamber", chambers)
    print("test_slot", test_slot)

    settings_info = dict()
    settings = get_settings(100)
    for item in settings:
        if item["name"] == 'product_name':
            settings_info['product_name'] = item["value"]
        elif item["name"] == 'station':
            settings_info['station'] = item["value"]

    block_title = '{}_{}'.format(
        settings_info['product_name'], settings_info['station'])

    return render_template('distribution_purge_release.html', form_data=data, station=info['station'], tests=test_slot, info=info, block_title=block_title, chambers=chambers, len=len(chambers))


@app.route('/get_json_forpurge/')
def get_json_forpurge():

    repo_slot = request.args.get('proglang', 0, type=str)
    print("repo_slot", repo_slot)

    with open(release_version_json_path) as json_file:
        # with open('/opt/Robot/release_version.json') as json_file:
        json_decoded = json.load(json_file)
        print(json_decoded[repo_slot]["release_path_version"])

        release_purge = json_decoded[repo_slot]["release_path_version"]

    return render_template('distribution_jsonpurge.html', release_purge=release_purge)


@app.route('/distribution/purge_release/', methods=['POST'])
def submit_purge_release(form_data=None):
    if form_data:
        data = form_data
    else:
        data = {}

    repo_slot = (str(request.form.get('repo_slot')))
    purge = (str(request.form.get('purge')))

    print("repo_slot", repo_slot)
    print("purge", purge)

    info = dict()
    settings = get_settings(100)
    for item in settings:
        if item["name"] == 'station':
            info['station'] = item["value"]
        elif item["name"] == 'model_test':
            info['model_test'] = item["value"]

    # folder = purge
    # for filename in os.listdir('/opt/Robot/'+folder):
    #     file_path = os.path.join('/opt/Robot/'+folder, filename)
    #     print("file_path",purge)
    #     try:
    #         if os.path.isfile(file_path) or os.path.islink(file_path):
    #             os.unlink(file_path)
    #         elif os.path.isdir(file_path):
    #             shutil.rmtree(file_path)
    #     except Exception as e:
    #         print('Failed to delete %s. Reason: %s' % (file_path, e))

    # os.rmdir('/opt/Robot/'+purge)

    # os.remove('/opt/Robot/{}.tar.gz'.format(purge))
    # os.remove('{}.tar.gz'.format(purge))

    if info['model_test'] == "sub-slot":

        if repo_slot[:7] == 'chamber':
            with open(release_version_json_path) as json_file:
                # with open('/opt/Robot/release_version.json') as json_file:
                json_decoded = json.load(json_file)
                print(json_decoded[repo_slot]["release_path_version"])

            json_decoded[repo_slot]["release_path_version"] = "empty"

            with open(release_version_json_path, 'w') as json_file:
                # with open('/opt/Robot/release_version.json', 'w') as json_file:
                json.dump(json_decoded, json_file)

        else:

            with open(release_version_json_path) as json_file:
                # with open('/opt/Robot/release_version.json') as json_file:
                json_decoded = json.load(json_file)
                print(json_decoded[repo_slot]["release_path_version"])

            json_decoded[repo_slot]["release_path_version"] = "empty"
            json_decoded[repo_slot+"_1"]["release_path_version"] = "empty"
            json_decoded[repo_slot+"_2"]["release_path_version"] = "empty"
            json_decoded[repo_slot+"_3"]["release_path_version"] = "empty"
            json_decoded[repo_slot+"_4"]["release_path_version"] = "empty"

            with open(release_version_json_path, 'w') as json_file:
                # with open('/opt/Robot/release_version.json', 'w') as json_file:
                json.dump(json_decoded, json_file)

    else:

        with open(release_version_json_path) as json_file:
            # with open('/opt/Robot/release_version.json') as json_file:
            json_decoded = json.load(json_file)
            print(json_decoded[repo_slot]["release_path_version"])

        json_decoded[repo_slot]["release_path_version"] = "empty"

        with open(release_version_json_path, 'w') as json_file:
            # with open('/opt/Robot/release_version.json', 'w') as json_file:
            json.dump(json_decoded, json_file)

        code_version = {"id": None, "location": repo_slot, "value": "empty"}
        put_release_version(code_version)

    info = dict()
    settings = get_settings(100)
    for item in settings:
        if item["name"] == 'station':
            info['station'] = item["value"]
        elif item["name"] == 'product_name':
            info['product_name'] = item["value"]

    block_title = '{}_{}'.format(info['product_name'], info['station'])

    print(info['station'])

    with open(release_version_json_path) as json_file:
        # with open('/opt/Robot/release_version.json') as json_file:
        json_decoded = json.load(json_file)
        print(json_decoded)

        slot = []
        slot_status = []

        for i in json_decoded:
            slot.append(i)

            slot_status.append(json_decoded[i]["release_path_version"])

    return render_template('distribution_home.html', form_data=data, slot=slot, slot_status=slot_status, station=info['station'], len1=len(slot), len2=len(slot_status), block_title=block_title)


@app.route('/purge_all_slot/')
def purge_all_slot():

    repo_slot = request.args.get('proglang', 0, type=str)
    print("purge_all_slot", repo_slot)

    info = dict()
    settings = get_settings(100)
    for item in settings:
        if item["name"] == 'station':
            info['station'] = item["value"]
        elif item["name"] == 'product_name':
            info['product_name'] = item["value"]
        elif item["name"] == 'chassis_name':
            info['chassis_name'] = item["value"]
        elif item["name"] == 'slot':
            info['slot'] = int(item["value"])
        elif item["name"] == 'model_test':
            info['model_test'] = item["value"]
        elif item["name"] == 'chamber':
            info['chamber'] = item["value"]

    slot_all = []
    slot_status = []
    slot = []

    chamber_all = []

    if info['model_test'] == "sub-slot":

        print("SubSlot", info['chamber'])

        for i in range(info['slot']):
            print(info['chassis_name']+str(i+1))
            slot_all.append(info['chassis_name']+str(i+1))

        for idx, val in enumerate(slot_all):
            print(idx, val)
            with open(release_version_json_path) as json_file:
                # with open('/opt/Robot/release_version.json') as json_file:
                json_decoded = json.load(json_file)
                print(json_decoded[val]["release_path_version"])

            json_decoded[val]["release_path_version"] = "empty"
            json_decoded[val+"_1"]["release_path_version"] = "empty"
            json_decoded[val+"_2"]["release_path_version"] = "empty"
            json_decoded[val+"_3"]["release_path_version"] = "empty"
            json_decoded[val+"_4"]["release_path_version"] = "empty"

            with open(release_version_json_path, 'w') as json_file:
                # with open('/opt/Robot/release_version.json', 'w') as json_file:
                json.dump(json_decoded, json_file)

        if info['chamber'] != 0:
            for ii in range(int(info['chamber'])):
                print('chamber'+str(int(ii)+int(info['slot'])+1))
                # chamber_all.append(info['chassis_name']+(i+1))

        # for idy, valy in enumerate(slot_all):
        #     print(idy, valy)
                with open('release_version_json_path') as json_file:
                    # with open('/opt/Robot/release_version.json') as json_file:
                    json_decoded = json.load(json_file)
                    print(
                        json_decoded['chamber'+str(int(ii)+int(info['slot'])+1)]["release_path_version"])

                json_decoded['chamber'+str(int(ii)+int(info['slot'])+1)
                             ]["release_path_version"] = "empty"

                with open(release_version_json_path, 'w') as json_file:
                    # with open('/opt/Robot/release_version.json', 'w') as json_file:
                    json.dump(json_decoded, json_file)

    else:

        for i in range(info['slot']):
            print(info['chassis_name']+str(i+1))
            slot_all.append(info['chassis_name']+str(i+1))

        for idx, val in enumerate(slot_all):
            print(idx, val)
            with open(release_version_json_path) as json_file:
                # with open('/opt/Robot/release_version.json') as json_file:
                json_decoded = json.load(json_file)

            json_decoded[val]["release_path_version"] = "empty"

            with open(release_version_json_path, 'w') as json_file:
                # with open('/opt/Robot/release_version.json', 'w') as json_file:
                json.dump(json_decoded, json_file)

            code_version = {"id": None, "location": val, "value": "empty"}
            put_release_version(code_version)

            if info['chamber'] != 0:
                for ii in range(int(info['chamber'])):
                    print('chamberzzz'+str(int(ii)+int(info['slot'])+1))
                    chamber_all.append(
                        'chamber'+str(int(ii)+int(info['slot'])+1))

            # # for idy, valy in enumerate(slot_all):
            # #     print(idy, valy)
            #         with open(release_version_json_path) as json_file:
            #             # with open('/opt/Robot/release_version.json') as json_file:
            #             json_decoded = json.load(json_file)
            #             print(
            #                 json_decoded['chamber'+str(int(ii)+1)]["release_path_version"])

            #         json_decoded['chamber'+str(int(ii)+1)
            #                      ]["release_path_version"] = "empty"

            #         with open(release_version_json_path, 'w') as json_file:
            #             # with open('/opt/Robot/release_version.json', 'w') as json_file:
            #             json.dump(json_decoded, json_file)

            #         code_version = {"id": None, "location": 'chamber'+str(int(ii)), "value": "empty"}
            #         put_release_version(code_version)

            for idy, valy in enumerate(chamber_all):
                print(idy, valy)
                with open(release_version_json_path) as json_file:
                    # with open('/opt/Robot/release_version.json') as json_file:
                    json_decoded = json.load(json_file)

                json_decoded[valy]["release_path_version"] = "empty"

                with open(release_version_json_path, 'w') as json_file:
                    # with open('/opt/Robot/release_version.json', 'w') as json_file:
                    json.dump(json_decoded, json_file)

                code_version = {"id": None, "location": valy, "value": "empty"}
                put_release_version(code_version)

                for i in json_decoded:
                    slot.append(i)
                    slot_status.append(json_decoded[i]["release_path_version"])

    block_title = '{}_{}'.format(info['product_name'], info['station'])

    time.sleep(3)

    return render_template('distribution_home.html', slot=slot, slot_status=slot_status, station=info['station'], len1=len(slot), len2=len(slot_status), block_title=block_title)


@app.route('/distribution/resource_server/', methods=['GET'])
def resource_server(form_data=None):
    if form_data:
        data = form_data
    else:
        data = {}

    print("resource_server")

    # private token or personal token authentication
    gl = gitlab.Gitlab('http://10.196.66.66/git/',
                       private_token='449KCc3c_snVhFX16m8f', per_page=100)
    # gl = gitlab.Gitlab('http://110.164.64.68/',email='pkhanma@celestica.com',password='thesis767Tee',api_version=4)

    gl.auth()

    datagroup = []
    group = gl.groups.list(all=True)
    for groups in group:
        # print(project.id[536])
        print(groups.name)

        item = groups.name
        datagroup.append(item)

        info = dict()
        settings = get_settings(100)
        for item in settings:
            if item["name"] == 'station':
                info['station'] = item["value"]
            elif item["name"] == 'product_name':
                info['product_name'] = item["value"]
            elif item["name"] == 'station':
                info['station'] = item["value"]

        block_title = '{}_{}'.format(info['product_name'], info['station'])

    # config_file = 'firmware_config.json'

    # with open(config_file) as json_file:
    #     json_decoded = json.load(json_file)
    #     # print(json_decoded)

    #     for (k, v) in json_decoded.items():
    #        print("Key: " + k)
    #        print("Value: " + str(v))

    #        for (sk, sv) in v.items():
    #            print("Key1: " + sk)
    #            print("Value1: " + str(sv))

    #            path = sv["desination"].split("/")
    #            str_path1 = path[0]
    #            str_path2 = path[1]
    #            print("path: " + str_path1)

    #            path_upload = str_path1
    # root = ET.parse(config_file).getroot()

    # for type_tag in root.findall('release_name'):
    #     release_name = type_tag.get('name')
    #     print(release_name)

    return render_template('resource_server.html', form_data=data, datagroup=datagroup, len3=len(datagroup), block_title=block_title)


@app.route('/get_dropdown_images/')
def get_dropdown_images():

    list_select = request.args.get('proglang', 0, type=str)
    print("list_select", list_select)

    config_file = path_global+'/'+tag_global+'/firmware_config.json'

    with open(config_file) as json_file:
        json_decoded = json.load(json_file)
        # print(json_decoded)

        images_list = []

        for (k, v) in json_decoded.items():
            print("Key: " + k)
            print("Value: " + str(v))

            for (sk, sv) in v.items():
                print("Key1: " + sk)
                print("Value1: " + str(sv))

                for (skt, svt) in sv.items():

                    print("Key2: " + skt)
                    print("Value2: " + str(svt))

                    path = svt["desination"].split("/")
                    print(path)
                    images_folder = path[2]
                    print(images_folder)
                    if images_folder != '':
                        if images_folder not in images_list:
                            images_list.append(images_folder)

                # print("path: " + path[1])

                # for (ssk, ssv) in sv.items():
                #     print("Key2: " + ssk)
                #     print("Value2: " + str(ssv))

    print(images_list)

    # images_list = ['BIC','BIOS','BMC','CPLD','FPGA','OOB_SW']

    return render_template('resource_images.html', images_list=images_list, len1=len(images_list))


@app.route('/get_dropdown_cpld/')
def get_dropdown_cpld():

    cpld_select = request.args.get('proglang', 0, type=str)
    print("cpld_select", cpld_select)

    config_file = path_global+'/'+tag_global+'/firmware_config.json'

    with open(config_file) as json_file:
        json_decoded = json.load(json_file)
        # print(json_decoded)

        cpld_list = []

        for (k, v) in json_decoded.items():
            print("Key: " + k)
            print("Value: " + str(v))

            for (sk, sv) in v.items():
                print("Key1: " + sk)
                print("Value1: " + str(sv))

                for (skt, svt) in sv.items():

                    print("Key2: " + skt)
                    print("Value2: " + str(svt))

                    str_cpld = svt["desination"].split("/")
                    print("path_cplds: ", str_cpld)

                    ck_cpld = skt.split("/")
                    print(len(ck_cpld))
                    if len(ck_cpld) == 4:
                        print("ck_cpld: " + ck_cpld[2])
                        if ck_cpld[2] == "CPLD":
                            cpld_folder = str_cpld[3]
                            print(cpld_folder)
                            if cpld_folder != '':
                                if cpld_folder not in cpld_list:
                                    cpld_list.append(cpld_folder)

    print(cpld_list)

    # cpld_list = ['FCM','PWR','SCM','SMB']

    return render_template('resource_cpld.html', cpld_list=cpld_list, len=len(cpld_list))


@app.route('/get_resource_path/')
def get_resource_path():

    info = dict()
    settings = get_settings(100)
    for item in settings:
        if item["name"] == 'station':
            info['station'] = item["value"]

    station = info['station']

    resource_path = request.args.get('proglang', 0, type=str)
    print("resource_path", resource_path)
    print("path", os.path.dirname(os.path.abspath(__file__)))

    data = resource_path.split(",")

    # private token or personal token authentication
    gl = gitlab.Gitlab('http://10.196.66.66/git/',
                       private_token='449KCc3c_snVhFX16m8f', per_page=100)
    # gl = gitlab.Gitlab('http://110.164.64.68/',email='pkhanma@celestica.com',password='thesis767Tee',api_version=4)BSM_EEPROM_TOOLS

    gl.auth()

    repo = data[1]
    global tag_global
    global path_global
    path_global = dir_path
    tag_global = data[0]

    print(repo)
    print(tag_global)

    projects = gl.projects.list()
    for project in projects:
        print(project.name)

        if project.name == repo:
            id_project = project.id
            project = gl.projects.get(id_project)
            print("id_project", id_project)

            tags_list = project.tags.list()
            for tag_name in tags_list:

                print("tag pick", tag_global)
                if tag_global == tag_name.name:

                    web_url = json.dumps(tag_name.commit["web_url"])
                    print("URL", web_url)

                    str_url = web_url.split("/")
                    print("str_path1", str_url[4])
                    print("str_path2", str_url[5])

            url = 'wget -continue -O {0}/firmware_config.json --header "PRIVATE-TOKEN: 449KCc3c_snVhFX16m8f" "http://10.196.66.66/git/api/v4/projects/{1}/repository/files/Package%2ffirmware_config.json/raw?ref={2}" '.format(
                dir_path, id_project, tag_global)
            print("url", url)
            # url = 'git clone --depth 1 --branch Wedge400_2020.07.29-01 http://pkhanma:thesis767Tee@203.170.244.69/git/Robot-Framework/Wedge400-Project/Wedge400-C_BI_RDT_ESS_Stations./'
            proc = subprocess.Popen(
                url, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            time.sleep(5)

            # while proc.poll() is None:

            print(os.system('pwd'))
            print(tag_global)

            if not os.path.exists(path_global+'/'+tag_global):
                print("create", path_global+'/')
                os.makedirs(path_global+'/'+tag_global)
                # shutil.move(path_global+'/firmware_config.json',
                #             path_global+'/'+tag_global+'/firmware_config.json')
                shutil.copy(path_global+'/firmware_config.json',
                            path_global+'/'+tag_global+'/firmware_config.json')
                # os.replace('firmware_config.json', tag+'/firmware_config.json')
                time.sleep(3)

            shutil.copy(path_global+'/firmware_config.json',
                        path_global+'/'+tag_global+'/firmware_config.json')
                # os.replace('firmware_config.json', tag+'/firmware_config.json')
            time.sleep(3)

            os.remove(path_global+'/firmware_config.json')

            # shutil.copyfile('firmware_config.json', tag+'/firmware_config.json')
                # config_file = 'firmware_config.json'

            with open(path_global+'/'+tag_global+'/firmware_config.json') as json_file:
                # with open('firmware_config.json') as json_file:
                try:
                    json_decoded = json.load(json_file)
                    print(json_decoded)

                    if json_decoded == {}:
                        return render_template('popup_json_empty.html')
                    else:
                        product = []

                        for (k, v) in json_decoded.items():
                            print("Key: " + k)
                            print("Value: " + str(v))

                            for (sk, sv) in v.items():
                                print("Key1: " + sk)
                                print("Value1: " + str(sv))

                                for (skt, svt) in sv.items():

                                    print("Key2: " + skt)
                                    print("Value2: " + str(svt))

                                    path = svt["desination"].split("/")
                                    print(path)
                                    str_path1 = path[0]
                                    str_path2 = path[1]
                                    print("path: " + str_path2)

                                product.append(sk)
                except:  # includes simplejson.decoder.JSONDecodeError
                    print("Error json format")

                    return render_template('popup_fiemware_file.html')
                    #            path = str(ssv).split("/")
                    #            print(path)
                    #            # product = path[1]
                    #            # rev = path[2]
                    #            images_list.append(path)
                print(product)

    return render_template('resource_submit.html', product=product, len=len(product))


@app.route('/get_resource_group/')
def get_resource_group():

    group_select = request.args.get('proglang', 0, type=str)
    print("get_resource_group", group_select)

    gl = gitlab.Gitlab('http://10.196.66.66/git/',
                       private_token='449KCc3c_snVhFX16m8f', per_page=100)
    gl.auth()

    tags = []
    dataproject = []

    group = gl.groups.list(all=True)

    # first_group_project = group.projects.list()[0]
    # manageable_project = gl.projects.get(first_group_project.id, lazy=True)
    # print(manageable_project, "manageable_project")

    # datagroup = []

    for groups in group:

        # item = groups.name
        # datagroup.append(item)

        if groups.name == group_select:

            print("sub_group_id", groups.id)

            subgroups = gl.groups.get(groups.id).subgroups.list()
            # group = gl.groups.get(subgroups[3].id)
            print("sub_group", subgroups)

            # subgroups = groups.get(176).subgroups.list()

            repo = groups.projects.list()
            print(repo)

            for project in repo:
                item = project.name
                # item = project.name
                print(item)
                dataproject.append(item)

    return render_template('resource_repo.html', len2=len(dataproject), dataproject=dataproject)


@app.route('/get_path_action/')
def get_path_action():

    repo_select = request.args.get('proglang', 0, type=str)
    print("test", repo_select)

    datatag = []
    gl = gitlab.Gitlab('http://10.196.66.66/git/',
                       private_token='449KCc3c_snVhFX16m8f', per_page=100)
    gl.auth()

    datatest = []
    tags = []
    name_tag = []
    datatag = []

    projects = gl.projects.list()
    for project in projects:
        print(project.name)

        item = project.name
        datatest.append(item)

        if project.name == repo_select:
            tags = project.tags.list()
            print(tags)
            # print(len(tags))

            for tag_name in tags:
                # name_tag = tag_name.name.list()
                # print(tag_name)

                datatag.append(tag_name.name)

    print(datatag)
    print(len(datatag))

    return render_template('resource_path.html', len2=len(datatag), datatag=datatag)


@app.route('/get__resource_repo/')
def get__resource_repo():

    repo_select = request.args.get('proglang', 0, type=str)
    print("get__resource_repo", repo_select)

    datatag = []
    gl = gitlab.Gitlab('http://10.196.66.66/git/',
                       private_token='449KCc3c_snVhFX16m8f', per_page=100)
    gl.auth()

    datatest = []
    tags = []
    name_tag = []
    datatag = []

    projects = gl.projects.list()
    for project in projects:
        # print(project.name)

        item = project.name
        datatest.append(item)

        if project.name == repo_select:
            tags = project.tags.list()
            print(tags)
            # print(len(tags))

            for tag_name in tags:
                # name_tag = tag_name.name.list()
                # print(tag_name)

                datatag.append(tag_name.name)

    print(datatag)
    print(len(datatag))

    return render_template('distribution_tag.html', len2=len(datatag), datatag=datatag)


@app.route('/distribution/resource_table/')
def resource_table(form_data=None):
    if form_data:
        data = form_data
    else:
        data = {}

    print("resource_table"+tag_global)

    config_file = path_global+'/'+tag_global+'/firmware_config.json'
    print("check_resource", tag_global)

    info = dict()
    settings = get_settings(100)
    for item in settings:
        if item["name"] == 'station':
            info['station'] = item["value"]
        elif item["name"] == 'product_name':
            info['product_name'] = item["value"]
        elif item["name"] == 'station':
            info['station'] = item["value"]

    block_title = '{}_{}'.format(info['product_name'], info['station'])

    with open(config_file) as json_file:
        json_decoded = json.load(json_file)

        for (k, v) in json_decoded.items():
            print("Key: " + k)
            print("Value: " + str(v))

            release_version = k

            resource_path = []
            file_resource = []
            package = []

            for (sk, sv) in v.items():
                print("Key1: " + sk)
                s = 0

                for (skt, svt) in sv.items():
                    package.append(sk)
                    print("Key2: " + skt)
                    print("Value2: " + str(svt))

                    s = s+len(svt)
                    print("lensss: {}".format(s))

                    desination = svt['desination']
                    file_source = svt['file']

                    resource_path.append(desination)
                    file_resource.append(file_source)

                    print(resource_path)
                    print(file_resource)

                    if "," not in file_source:
                        file_pac = file_source
                        print(type(file_source))

                        remote_images_path = '/home/export/resource/'+sk+desination
                        local_path = robot_root_path+k+'/Package/Products/'+sk+desination

                        print("remote_images_path"+remote_images_path+file_pac)
                        print("local_path"+local_path+file_pac)

                        ssh_client = paramiko.SSHClient()
                        ssh_client.set_missing_host_key_policy(
                            paramiko.AutoAddPolicy())
                        ssh_client.connect(hostname="10.196.66.71", username="disserver",
                                           password="tde123Admin")
                        sftp = ssh_client.open_sftp()

                        try:
                            sftp.chdir(remote_images_path)

                        except:
                            print("remote_images_path.errno")
                            flash('Package: '+sk+' No have directory in' +
                                  desination+', Please upload file before', 'danger')

                        try:

                            print(sftp.stat(remote_images_path+file_pac))
                            print('file exists')
                        except:
                            print("e.errno")
                            flash('No have '+file_pac+' in '+desination +
                                  ', Please upload file before', 'danger')

                        sftp.close()
                        ssh_client.close()

                    else:
                        file_source = svt['file'].split(",")
                        print(file_source)

                        for idx, item in enumerate(file_source):
                            print(item)

                            remote_images_path = '/home/export/resource/'+sk+desination
                            local_path = robot_root_path+k+'/Package/Products/'+sk+desination

                            print("remote_images_path"+remote_images_path+item)
                            print("local_path"+local_path+item)

                            ssh_client = paramiko.SSHClient()
                            ssh_client.set_missing_host_key_policy(
                                paramiko.AutoAddPolicy())
                            ssh_client.connect(hostname="10.196.66.71", username="disserver",
                                               password="tde123Admin")
                            sftp = ssh_client.open_sftp()

                            try:
                                sftp.chdir(remote_images_path)

                            except:
                                print("remote_images_path.errno")
                                flash('Package: '+sk+' No have directory in' +
                                      desination+', Please upload file before', 'danger')

                            try:

                                print(sftp.stat(remote_images_path+item))
                                print('file exists')
                            except:
                                print("e.errno")
                                flash('No have '+item+' in '+desination +
                                      ', Please upload file before', 'danger')

                            sftp.close()
                            ssh_client.close()

        print("package", package)

    return render_template('resource_check_file.html', form_data=data, release_version=release_version, resource_path=resource_path, file_resource=file_resource, len=len(resource_path), block_title=block_title, package=package)


@app.route('/log/')
def log():
    logs_data = view_all_log("")
    settings_info = dict()
    settings = get_settings(100)
    for item in settings:
        if item["name"] == 'product_name':
            settings_info['product_name'] = item["value"]
        elif item["name"] == 'station':
            settings_info['station'] = item["value"]

    block_title = '{}_{}'.format(
        settings_info['product_name'], settings_info['station'])

    # print('Logs_data : ' + str(logs_data))

    return render_template('log.html', logs=logs_data, block_title=block_title)


@app.route('/log/', methods=['POST'])
def page_log_with_filter():
    logs_filter = request.form.to_dict()
    print(logs_filter)
    logs_data = view_log_with_filter(logs_filter)

    settings_info = dict()
    settings = get_settings(100)
    for item in settings:
        if item["name"] == 'product_name':
            settings_info['product_name'] = item["value"]
        elif item["name"] == 'station':
            settings_info['station'] = item["value"]

    block_title = '{}_{}'.format(
        settings_info['product_name'], settings_info['station'])

    return render_template('log.html', logs=logs_data, filter=logs_filter, block_title=block_title)


@app.route('/log/download/<string:filename>')
def download(filename):
    path = get_path_log()
    # new format filename ISS_pass_Pre-FCT_20190528074511.zip
    if len(filename.split('_')) > 1:
        date = filename.split(".")[0].split("_")[-1]
        date_folder = "%s-%s-%s" % (date[0:4], date[4:6], date[6:8])
    else:
        abort(404)
    directory = join(path, date_folder)
    return send_from_directory(directory=directory, path=path, filename=filename)


@app.route('/log/<string:filename>/')
def view_log_from_filename(filename):
    # new format filename ISS_pass_Pre-FCT_20190528074511.zip
    if len(filename.split('_')) > 1:
        date = filename.split(".")[0].split("_")[-1]
        date_folder = "%s-%s-%s" % (date[0:4], date[4:6], date[6:8])
    else:
        abort(404)
    info_log, status = view_log(date_folder, filename)
    if status != 200:
        abort(404)
    print(info_log['data']["statuses"])
    # return send_from_directory(directory=path[0]['data'].replace('/log.html',''),filename=file_name)
    raw_statuses = info_log['data']["statuses"]
    setting = get_setting_by_name('chassis_name')

    if(setting):
        chassis_name = setting['value']
    else:
        chassis_name = ''
    slot_no = 0
    statuses = list()
    info = {'result': info_log['data']['result'], 'slot_no': slot_no,
            'chassis_name': chassis_name, 'filename': filename}
    if len(raw_statuses) == 0:
        abort(404)
    for index, item in enumerate(raw_statuses):
        if item["status"] == 'start_test':
            statuses.append({'name': item['message'], 'status': 'Testing',
                             'started': item['created'], 'finished': None, 'elapsed_time': '', 'reason': ''})
        elif item["status"] == 'end_test':
            msg = item['message'].split(' ', 1)
            statuses[-1]['status'] = msg[0].replace("Result:", "")
            if statuses[-1]['status'] == "PASS":
                statuses[-1]['status'] = "passes"
            elif statuses[-1]['status'] == "ABORT":
                statuses[-1]['status'] = "aborted"
            else:
                statuses[-1]['status'] = "failed"

            info["result"] = statuses[-1]['status']

            if len(msg) > 1:
                statuses[-1]['reason'] = msg[1]
            else:
                statuses[-1]['reason'] = '-'
            statuses[-1]['finished'] = item['created']
            elapsed_time = datetime.datetime.strptime(
                statuses[-1]['finished'], "%Y-%m-%d %H:%M:%S") - datetime.datetime.strptime(
                statuses[-1]['started'], "%Y-%m-%d %H:%M:%S")
            statuses[-1]['elapsed_time'] = str(elapsed_time).split('.')[0]
        elif item["status"] == 'end_suit':
            print("\nStatuses : " + statuses[-1]['status'])
            info["result"] = statuses[-1]['status']
        else:
            print(index, item)

    settings_info = dict()
    settings = get_settings(100)
    for item in settings:
        if item["name"] == 'product_name':
            settings_info['product_name'] = item["value"]
        elif item["name"] == 'station':
            settings_info['station'] = item["value"]

    block_title = '{}_{}'.format(
        settings_info['product_name'], settings_info['station'])

    return render_template('log_status.html', statuses=statuses, info=info, block_title=block_title)


@app.route('/log/<string:filezip>/view/<string:filename>')
def view_filename_in_zipfile(filezip=None, filename=None):
    settings_info = dict()
    settings = get_settings(100)
    for item in settings:
        if item["name"] == 'product_name':
            settings_info['product_name'] = item["value"]
        elif item["name"] == 'station':
            settings_info['station'] = item["value"]

    block_title = '{}_{}'.format(
        settings_info['product_name'], settings_info['station'])

    raw_logs = view_log_rawlog(filezip, filename)
    sequence_logs = view_log_sequencelog(filezip, filename)

    return render_template('view_log.html', raw_logs=raw_logs, sequence_logs=sequence_logs, filename=filename, block_title=block_title)

# Custom static data
@app.route('/interaction_images/<string:filename>/<path:filepath>')
def interaction_files(filename, filepath):
    filepath = '/{}'.format(filepath)
    return send_from_directory(filepath, filename)


@app.route('/playbox/')
def playbox():
    info = dict()
    test_slot = dict()
    settings = get_settings(100)
    logops = get_logop(100)

    for item in settings:
        if item["name"] == 'slot':
            info['slot'] = int(item["value"])
        elif item["name"] == 'product_name':
            info['product_name'] = item["value"]
        elif item["name"] == 'operation':
            info['operation'] = item["value"]
        elif item["name"] == 'chassis_name':
            info['chassis_name'] = item["value"]
        elif item["name"] == 'station':
            info['station'] = item["value"]
        elif item["name"] == 'parameter':
            info['parameter'] = item["value"]
        elif item["name"] == 'interval':
            info['interval'] = int(item["value"])
        elif item["name"] == 'log_template':
            info['log_template'] = item["value"]
        elif item["name"] == 'version':
            info['version'] = item["value"]
        elif item["name"] == 'model_test':
            info['model_test'] = item["value"]

    if info['model_test'] == "sub-slot":
        for i in range(1, info['slot']+1):
            test_slot[str(i)] = info['chassis_name'] + str(i)
            test_slot['{}_1'.format(str(i))] = '{}_1'.format(
                info['chassis_name'] + str(i))
            test_slot['{}_2'.format(str(i))] = '{}_2'.format(
                info['chassis_name'] + str(i))
            test_slot['{}_3'.format(str(i))] = '{}_3'.format(
                info['chassis_name'] + str(i))
            test_slot['{}_4'.format(str(i))] = '{}_4'.format(
                info['chassis_name'] + str(i))
    else:
        for i in range(1, info['slot']+1):
            test_slot[str(i)] = info['chassis_name'] + str(i)

    print(test_slot)

    tests = get_tests(100)
    for item in tests:
        print(item["location"])
        del test_slot[item["location"]]

    block_title = '{}_{}'.format(
        info['product_name'], info['station'])

    return render_template('playbox.html', info=info, test_slot=test_slot, logops=logops, block_title=block_title)


@app.route('/playbox/', methods=['POST'])
def page_playbox_with_verify():
    info = dict()
    test_slot = list()
    settings = get_settings(100)

    playbox_verify = request.form.to_dict()

    # print("Setting {}".format(settings))
    for item in settings:
        if item["name"] == 'slot':
            info['slot'] = int(item["value"])
        elif item["name"] == 'product_name':
            info['product_name'] = item["value"]
        elif item["name"] == 'operation':
            info['operation'] = item["value"]
        elif item["name"] == 'chassis_name':
            info['chassis_name'] = item["value"]
        elif item["name"] == 'station':
            info['station'] = item["value"]
        elif item["name"] == 'parameter':
            info['parameter'] = item["value"]
        elif item["name"] == 'interval':
            info['interval'] = int(item["value"])
        elif item["name"] == 'log_template':
            info['log_template'] = item["value"]
        elif item["name"] == 'version':
            info['version'] = item["value"]
        elif item["name"] == 'model_test':
            info['model_test'] = item["value"]

    block_title = '{}_{}'.format(
        info['product_name'], info['station'])

    for i in range(1, info['slot']+1):
        test_slot.append(dict())
        test_slot[i-1] = info['chassis_name'] + str(i)

    release_version = get_release_version_by_location(
        playbox_verify["slot_location"])
    playbox_verify["robot_path"] = release_version['value']

    if playbox_verify["robot_path"] == 'empty' and playbox_verify["code_from"] == "Production":
        error_message = "Cannot found robot file please zone your robot file to slot {}".format(
            playbox_verify["slot_location"])
        return render_template('playbox.html', info=info, test_slot=test_slot, playbox_verify=playbox_verify, error_message=error_message)


    tests = get_tests(100)

    test_get_data = verify_testcase(playbox_verify)
    print(test_get_data)

    for item in tests:
        del test_slot[int(item["location"])-1]

    path_to_test_suite = "{}/{}_{}_{}.robot".format(test_get_data["robot_path"],
                                                    test_get_data["part_number"], test_get_data["product_reversion"], playbox_verify["logop"])

    if not os.path.exists(path_to_test_suite):
        error_message = "Cannot found robot file please create robot file {} reset and try again.".format(
            path_to_test_suite)
        return render_template('playbox.html', info=info, test_slot=test_slot, playbox_verify=playbox_verify, error_message=error_message)

    testcase_name = list()
    # path_to_test_suite = test_slot['robot_name']
    suites = TestData(parent=None, source=path_to_test_suite)
    for testcase in suites.testcase_table:
        testcase_name.append(testcase.name)

    return render_template('playbox.html', info=info, testcases=testcase_name, test_slot=test_slot, playbox_verify=playbox_verify, block_title=block_title)


@application.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404


@application.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@application.before_first_request
def setup(exception=None):
    database.populate()


@application.before_request
def before_request():
    g.socket = socketio


@application.teardown_appcontext
def teardown_db(exception):
    socket = g.pop('socket', None)


def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.getenv('PORT'), debug=False)


# @socketio.on('my event')
# def handle_my_custom_event(json, methods=['GET', 'POST']):
#     print('received my event: ' + str(json))
#     socketio.emit('my response', json, callback=messageReceived)


# if __name__ == '__main__':
#     socketio.run(application, host='0.0.0.0',
#                  port=os.getenv('PORT'), debug=False)
