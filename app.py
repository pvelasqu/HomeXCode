from flask import Flask, render_template
import pymysql
import json
import yaml
import requests


with open("config.yaml", 'r') as config_file:
    config_yaml = yaml.load(config_file)

db = pymysql.connect(config_yaml['mysql']['host'], config_yaml['mysql']['user'], config_yaml['mysql']['passwd'],
                     config_yaml['mysql']['db'])

app = Flask(__name__)


def get_activity_to_id(cursor):
    """
    Creates and returns a dictionary which shows the relationship between an activity ID and the activity name
    :param cursor: db.cursor to perform SQL queries
    :return: dictionary which is contains activity name to activity ID
    :rtype: dict
    """
    activity_to_id_query = "SELECT id, name FROM activities"
    cursor.execute(activity_to_id_query)
    activity_to_id_results = cursor.fetchall()

    activity_to_id_dict = dict()
    for each_activity in activity_to_id_results:
        activity_to_id_dict[each_activity[0]] = each_activity[1]

    return activity_to_id_dict


def make_hierarchy_dict(list_child_parent, activity_to_id_rel, workers_to_activity_rel):
    """

    :param list_child_parent: List of all parent and child activities in the DB.
    :param activity_to_id_rel: Dictionary which contains the activity to ID relationship
    :param workers_to_activity_rel: Dictionary which contains the person ID to activity
    :return: JSON dump of the hierarchy of the jobs.
    :rtype: object
    """
    has_parent = set()
    all_items = {}
    for child, parent in list_child_parent:
        if activity_to_id_rel[parent] not in all_items:
            if str(parent) in workers_to_activity_rel:
                workers = workers_to_activity_rel[str(parent)]
            else:
                workers = []
            all_items[activity_to_id_rel[parent]] = {'Workers': workers}
        if activity_to_id_rel[child] not in all_items:
            if str(child) in workers_to_activity_rel:
                workers = workers_to_activity_rel[str(child)]
            else:
                workers = []
            all_items[activity_to_id_rel[child]] = {'Workers': workers}
        all_items[activity_to_id_rel[parent]][activity_to_id_rel[child]] = all_items[activity_to_id_rel[child]]
        has_parent.add(activity_to_id_rel[child])

    result = {}
    for key, value in all_items.items():
        if key not in has_parent:
            result[key] = value
    return result


def request_workers(person_id):
    request_string = 'http://interview.homex.io/api/people/{id}'.format(id=person_id)
    worker_name = requests.get(request_string).json()['name']
    return worker_name


def get_workers_to_activity(cursor):
    """
    Gets the worker IDs to the Activity ID they are tied in. Key is the Activity ID and Value is a list of workers which
    belong to that activity.

    TODO: Tie the Worker ID to a Worker Name if the API per the instructions as available. E.G:
    http://interview.homex.io/api/people/{person_id}
    :param cursor: db.cursor to perform SQL queries
    :return: Dictionary which contains the relationship between activity and the workers from that activity.
    """
    workers_to_activity_query = "SELECT activity_id, person_id from activities_people"

    workers_activity_dict = dict()

    cursor.execute(workers_to_activity_query)
    workers_to_activity_result = cursor.fetchall()

    for activity, worker in workers_to_activity_result:
        if str(activity) in workers_activity_dict:
            workers_activity_dict[str(activity)] = workers_activity_dict[str(activity)] + [request_workers(str(worker))]
        else:
            workers_activity_dict[str(activity)] = [request_workers(str(worker))]

    return workers_activity_dict


def get_json_data():
    """
    Executes the logic to getting the JSON data in a hierarchical data
    :return: dict dump of the data
    """
    cursor = db.cursor()
    activity_to_id_dict = get_activity_to_id(cursor)
    hierarchy_query = "SELECT id, parent_activity_id FROM activities where parent_activity_id is not NULL"
    cursor.execute(hierarchy_query)
    hierarchy_results = cursor.fetchall()
    hierarchy_dict = make_hierarchy_dict(hierarchy_results, activity_to_id_dict, get_workers_to_activity(cursor))
    return hierarchy_dict


@app.route('/')
def render_home():
    result = get_json_data()
    return render_template('index.html', result=result)


@app.route('/json')
def return_hierarchy_json():
    result = get_json_data()
    print(json.dumps(result, sort_keys=False, indent=4, separators=(',', ': ')))
    return json.dumps(result)


if __name__ == '__main__':
    app.run(debug=True)
