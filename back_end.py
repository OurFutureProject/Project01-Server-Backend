from flask import (Flask, jsonify, request, Response, render_template,
                   send_from_directory)
from functools import wraps
from json import dumps
import time


app = Flask(__name__)

def server_run():
    '''Run server.
    '''
    global user_list
    user_list = {}
    with open("storage/User.json") as file:
        for line in file:
            (key, val) = line.split()
            user_list[key] = val
    app.run(host='0.0.0.0')

@app.route('/favicon.ico')
def favicon():
    '''Favicon for webpage
    @return a icon for webpage
    '''
    return send_from_directory(os.path.join(app.root_path, 'static/favicon'),
                               'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')

@app.route('/verify_user/<username>/<password>')
def verify_user(username, password):
    '''Verify whether username/password combo exists in system
    @return EOK if combo exists, EFAULT if otherwise
    '''
    global user_list
    if username in user_list:
        if user_list[username] == password:
            return 'EOK'
    return 'EFAULT'


@app.route('/create_user/<username>/<password>')
def create_user(username, password):
    '''Create a new user for validation purpose
    @return EOK if creation is successful, EFAULT if username already exists
    '''
    global user_list
    if username in user_list:
        return 'EFAULT'
    user_list[username] = password
    with open("storage/User.json", "w") as file:
        file.write(username + " " + password)
    return 'EOK'

@app.route('/home')
def display_default_home():
    '''Display homepage
    @return render a home page
    '''
    return render_template('home.html')
