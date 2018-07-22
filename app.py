from flask import Flask, request, render_template
import pymysql

db = pymysql.connect("localhost", "root", "hello", "homex_test")

app = Flask(__name__)


def get_activity_to_id(cursor):
    activity_to_id_query = "SELECT id, name FROM activities"
    cursor.execute(activity_to_id_query)
    activity_to_id_results = cursor.fetchall()

    activity_to_id_dict = dict()
    for each_activity in activity_to_id_results:
        activity_to_id_dict[each_activity[0]] = each_activity[1]

    return activity_to_id_dict

def generate_json_hierarchy_dump(hierarchial_dict):
    dictionary = dict()


@app.route('/')
def render_home():
    cursor = db.cursor()
    activity_to_id_dict = get_activity_to_id(cursor)
    hierarchy_query = "SELECT * FROM activities"
    cursor.execute(hierarchy_query)
    hierarchy_results = cursor.fetchall()
    hierarchical_dictionary = dict()

    for each_activity in hierarchy_results:
        if each_activity[2] is None:
            hierarchical_dictionary[activity_to_id_dict[each_activity[0]]] = []
        elif activity_to_id_dict[each_activity[2]] in hierarchical_dictionary:
            hierarchical_dictionary[activity_to_id_dict[each_activity[2]]] = \
                hierarchical_dictionary[activity_to_id_dict[each_activity[2]]] + [activity_to_id_dict[each_activity[0]]]
        else:
            hierarchical_dictionary[activity_to_id_dict[each_activity[2]]] = [activity_to_id_dict[each_activity[0]]]
    print(hierarchical_dictionary)
    return render_template('index.html', results=hierarchy_results)


if __name__ == '__main__':
    app.run(debug=True)
