from flask import *
import jsonpickle
from flask import Flask, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo
import bcrypt
from hashlib import md5
from flask_login import current_user, login_user
from flask_security import login_required
from flask import Flask
from flask import request
from flask import Flask, jsonify
from flask import abort
from flask_pymongo import PyMongo
import os
from bson.json_util import dumps
from flask import Flask, render_template, url_for, json, request, flash, redirect
import json
import requests
from werkzeug import secure_filename
import os
import pickle
import sys
import csv
import time
import sys
import datetime
from flask_login import LoginManager

from jinja2 import Environment, PackageLoader
from flask import make_response, flash
from flask import session as login_session

from flask import abort
from flask import make_response
from flask import request
from flask import url_for
import json
from bson import json_util
import os
# add mongo db alta


import pprint

from werkzeug.routing import BaseConverter, ValidationError
from itsdangerous import base64_encode, base64_decode
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import urllib, json

import httplib2
import json
import requests
import random
import string
from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, IntegerField, TextAreaField, validators, StringField, SubmitField
import logging
from transitions import Machine
import random
from insightly import Insightly

debug=True

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://naruto45me:N%40ruto45me@ds062448.mlab.com:62448/keytechlabs'

mongo = PyMongo(app)
########################
# Flask Server Example #
########################

##LEADERBOARD
## This will be a list with simple dict inside (eg. [{name: Joe, score: 10},{name: Jane, score: 20}])
logging.basicConfig(level=logging.DEBUG)
# Set transitions' log level to INFO; DEBUG messages will be omitted
logging.getLogger('transitions').setLevel(logging.INFO)
leaderboard = []
id = 0
@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('home'))

    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    users = mongo.db.users
    login_user = users.find_one({'name' : request.form['username']})
        
    if login_user:


        if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password'].encode('utf-8')) == login_user['password'].encode('utf-8'):
            session['username'] = request.form['username']
            
            return redirect(url_for('index'))

    return 'Invalid username/password combination'

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name' : request.form['username']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'name' : request.form['username'], 'password' : hashpass})
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        
        return 'That username already exists!'

    return render_template('register.html') 
# INDEX PAGE
@app.route('/leaderboard')
def home():
    lb_id= 0
    Users=mongo.db.users.find({})
    login_user = mongo.db.users.find_one({'name' : session['username']})
    return render_template('leaderboard.html', Users=Users, login_user=login_user)
  
# GET LEADERBOARD
@app.route('/api/getleaders')
def get_leader():
    global leaderboard
    print "Getting Leaderboard"
    print leaderboard
    return jsonpickle.encode(leaderboard)
 
# ADD ENTRY
@app.route('/api/addentry/',methods=['GET', 'POST'])
def add_entry():
    global leaderboard,id
    print "Adding Entry"
    if request.method == 'POST':
        name = request.form['name']
        score = request.form['score']
        
    leaderboard += [{"id":id,"name":request.form['name'],"score":request.form['score']}]
    return redirect(url_for('home'))
 
# REMOVE ENTRY
@app.route('/api/rmentry/', methods=['DELETE'])
def rm_entry(entry_id):
    global leaderboard
    print "Removing Entry!"
 
    for entry in leaderboard:
        if entry["id"] == entry_id:
            leaderboard.remove(entry)
            break;
 
    return jsonpickle.encode(leaderboard)
 
@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)




@app.route('/divide_form')
def divide_form():
    return render_template('divide_form.html')

@app.route('/divide_result', methods=['POST'])
def divide_result():
    units = float(request.form['units'])
    cycle_time = float(request.form['cycle_time'])
    rate= float(request.form['rate'])
    software= float(request.form['software'])
    hardware= float(request.form['hardware'])
    return render_template('divide_result.html', result=(units*cycle_time*rate)+(software+hardware))


@app.route("/cal1", methods=['GET', 'POST'])
def Concole_cal1():
    counter = 0
    arry = []
    error = None
    rows = zip(arry)
    if request.method == 'POST':
        if request.form['username'] != 'admin' or \
                request.form['password'] != 'secret':
            error = 'Invalid credentials'
            flash('Invalid credentials')
            with open('wincsv5.csv') as csvfile:
                reader = csv.DictReader(csvfile)
        for row in reader:
            if new_name in row['CaseOwner']:
                    if row['License'] =='':
                        output = row['License'], row['Subject'], row['id']
                        ## by calling output we now can control the output into what is place in to arry and, down the line what is writen in to the csv
                        arry.append(str(output))
                        flash(output)
                        counter = counter+1
                        flash("count of all cases with the keyword:",'red'), colored(new_name, 'green'), colored(counter,'red')
        ##I learned how to use zip()! it helps package the array to be unpackage later by the for loop##
        else:
            flash('You were successfully logged in')
            return redirect(url_for('index'))
    return render_template('microtest3.html', error=error)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
            return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

#update a usecase
# @app.route('/Community/<int:community_id>/edit/', methods = ['GET','POST'])
# def editCommunity(community_id):
#   editedCommunity = session.query(Community).filter_by(id = community_id).one()
#   if request.method == 'POST':
#       if request.form['name']:
#         editedCommunity.name = request.form['name']
#       if request.form['info']:
#         editedCommunity.info = request.form['info']
#       if request.form['zipcode1']:
#         editedCommunity.zipcode1 = request.form['zipcode1']
#       if request.form['zipcode2']:
#         editedCommunity.zipcode2 = request.form['zipcode2']
#       if request.form['zipcode3']:
#         editedCommunity.zipcode3 = request.form['zipcode3']
#         session.add(editedCommunity)
#         session.commit() 
#         flash('Community Successfully Edited %s' % editedCommunity.name)
#         return redirect(url_for('showCommunity'))
#   else:
#     return render_template('Community_edit.html', community = editedCommunity)



@app.route('/support/diagrams/<int:data_ID>/', methods=['GET'])
def showdiagram(data_ID):
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "static/data", "diagrams.json")
    json_url2 = os.path.join(SITE_ROOT, "static/data", "columns2.json")
    dig = json.load(open(json_url))
    num  =int(data_ID)-2
    num2 = jsonify({'data': data[num]})
    num3 = data[num]
    columns2 =json.load(open(json_url2))

    return render_template('diagram_lexy.html', dig=dig, num=num, num2=num2,num3=num3, columns2=columns2)

@app.route('/support/diagrams')
def showdiagrams():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "static/data", "supportdiagrams.json")
    dig = json.load(open(json_url))
    return render_template('codec.html', dig=dig)
# Profile per Id
class ReusableForm(Form):
    name = TextField('Name:', validators=[validators.required()])
    ID = IntegerField('ID:')
    topic = TextField('topic:', validators=[validators.required()])
    version = TextField('version:')
    issue = TextField('issue:')
    solution = TextField('solution:')
    trigger = TextField('trigger:')
    alternatieflow = TextField('alternatieflow:')
    DOCS = TextField('documentation:')
   
    definiation = TextField('definiation:')
    deviceversion = TextField('deviceversion:')
    device = TextField('device:')
    def reset(self):
        blankData = MultiDict([ ('csrf', self.reset_csrf() ) ])
        self.process(blankData)

@app.route('/support/api/v1.0/support/profile/<int:data_ID>/', methods=['GET','POST'])
def get_data(data_ID):
    login_user = mongo.db.users.find_one({'name' : session['username']})

    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "static/data", "supportusecase.json")
    json_url2 = os.path.join(SITE_ROOT, "static/data", "supportcolumns.json")
    json_url3 = os.path.join(SITE_ROOT, "static/data", "supportdiagrams.json")
    mongos = mongo.db.UseCases.find()
    data = mongo.db.UseCases.find()
      
    datas = mongo.db.UseCases.find({})
    num = int(data_ID)-1
    num2 = {'data': data[num]}
    num3 = data[num]
    #switch to this to use json files instead of MongoDb json.load(open(json_url2))
    columns =mongo.db.columns.find()
    for doc in columns:
        columns = [doc]
    dig=mongo.db.diagrams.find()
    all_cases_counter = 0
    Number_of_worflow = 0
    # endpoint to update data from FORM
    # form post
    form = ReusableForm(request.form)
    
    if request.method == 'POST' and "units" in request.form:
        units = float(request.form['units'])
        cycle_time = float(request.form['cycle_time'])
        rate= float(request.form['rate'])
        software= float(request.form['software'])
        hardware= float(request.form['hardware'])
        results = (units*cycle_time*rate)+(software+hardware)
    else:
        results = 0
        units = 0
        cycle_time = 0
        rate = 0
        software = 0
        hardware = 0


    if request.method == 'POST' and "name" in request.form:
        name=request.form['name']
        ID= int(request.form['ID']) 
        topic=request.form['topic']
        DOCS=request.form['DOCS']
        
        issue=request.form['issue']
        solution=request.form['solution']


        with open('static/data/supportusecase.json', "r+") as jsonfile:
                
            update = json.load(jsonfile)
            row = ID - 1
           

            tmp = update[row]["SUBJECT"]
            update[row]["SUBJECT"] = name
            jsonfile.seek(0)  # rewind
            tmp2 = update[row]["ID"]
            update[row]['ID'] = ID
            jsonfile.seek(0)  # rewind
            tmp3 = update[row]["TOPIC"]
            update[row]["TOPIC"] = topic
            jsonfile.seek(0)  # rewind
            tmp3 = update[row]["DOCS"]
            update[row]["DOCS"] = DOCS
            jsonfile.seek(0)  # rewind
            tmp3 = update[row]["ISSUE"]
            update[row]["ISSUE"] = issue
            jsonfile.seek(0)  # rewind
            tmp3 = update[row]["SOLUTION"]
            update[row]["SOLUTION"] = solution

            jsonfile.seek(0)  # rewind
            json.dump(update, jsonfile)
            jsonfile.truncate()

        if form.validate():
            # Save the comment here.
            flash('Hello ' + name)
        else:
            flash('Error: All the form fields are required. ')
    #end of update endpoint
    
    with open('static/data/wincsv5.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            all_cases_counter = all_cases_counter+1
    #with open('/static/data/usecase.json', 'w') as data_file:
     #   json.dump(request.form, data_file)

    return render_template('support.html', login_user=login_user, units = units, cycle_time=cycle_time,rate=rate,software=software,hardware=hardware, results=results , num2=num2, mongos=mongos, reader=reader,datas=datas, data=data, num=num, num3=num3, columns=columns, dig=dig, all_cases_counter=all_cases_counter, Number_of_worflow=Number_of_worflow, form=form)


@app.route('/support/usecases')
def showjson():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "static/data", "supportusecase.json")
    json_url2 = os.path.join(SITE_ROOT, "static/data", "supportcolumns.json")
    # csv to Json

    # json join to json
    #dictA = json.loads(json_url)
   # dictB = json.loads(json_url2)
    #merged_dict = {key: value for (key, value) in (dictA.items() + dictB.items())}
    # string dump of the merged dict
    #jsonString_merged = json.dumps(merged_dict)    
    #add to data
    data = json.load(open(json_url))
    columns =json.load(open(json_url2))
    




    return render_template('supportresults.html', data=data, columns = columns)



@app.route('/support/api/v1.0/usecase', methods=['GET'])
def get_usecases():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "static/data", "supportusecase.json")
    data = json.load(open(json_url))
    return jsonify({'data': data})
#read api per ID
@app.route('/support/api/v1.0/usecase/<int:data_ID>', methods=['GET'])
def get_usecase(data_ID):
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "static/data", "supportusecase.json")
    data = json.load(open(json_url))
    num  =int(data_ID)-1
    return jsonify({'data': data[num]})

# @app.route('/support/api/v1.0/usecase/profile/<int:data_ID>/', methods=['GET'])
# def get_usecaseprofile(data_ID):
#   SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
#   json_url = os.path.join(SITE_ROOT, "static/data", "usecase.json")
#   json_url2 = os.path.join(SITE_ROOT, "static/data", "columns.json")
#   data = json.load(open(json_url))
#   num  =int(data_ID)-1
#   columns =json.load(open(json_url2))
#   return render_template()


@app.route('/onboarding/api/v1.0/onboarding/profile/<int:data_ID>/', methods=['GET','POST'])


def onboarding_get_data(data_ID):
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "static/data", "onboardingusecase.json")
    json_url2 = os.path.join(SITE_ROOT, "static/data", "onboardingcolumns.json")
    json_url3 = os.path.join(SITE_ROOT, "static/data", "onboardingdiagrams.json")
    units = float(request.form['units'])
    cycle_time = float(request.form['cycle_time'])
    rate= float(request.form['rate'])
    software= float(request.form['software'])
    hardware= float(request.form['hardware'])
    
    #data = #mongo.db.UseCases.find()
    datas = dumps(data)
    num = int(data_ID)-1
    #num2 = jsonify({'data': data[num]})
    #num3 = data[num]
    columns =json.load(open(json_url2))
    dig=json.load(open(json_url3))
    all_cases_counter = 0
    Number_of_worflow = 0
    # endpoint to update data from FORM
    # form post
    form = ReusableForm(request.form)
    

    if request.method == 'POST' and "name" in request.form:
        name=request.form['name']
        ID= int(request.form['ID']) 
        topic=request.form['topic']

        with open('static/data/onboardingusecase.json', "r+") as jsonfile:
            update = json.load(jsonfile)
            row = ID - 1
           

            tmp = update[row]["SUBJECT"]
            update[row]["SUBJECT"] = name
            jsonfile.seek(0)  # rewind
            tmp2 = update[row]["ID"]
            update[row]['ID'] = ID
            jsonfile.seek(0)  # rewind
            tmp3 = update[row]["TOPIC"]
            update[row]["TOPIC"] = topic

            jsonfile.seek(0)  # rewind
            json.dump(update, jsonfile)
            jsonfile.truncate()

        if form.validate():
            # Save the comment here.
            flash('Hello ' + name)
        else:
            flash('Error: All the form fields are required. ')
    #end of update endpoint
    
    with open('static/data/wincsv5.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            all_cases_counter = all_cases_counter+1
    #with open('/static/data/usecase.json', 'w') as data_file:
     #   json.dump(request.form, data_file)

    return render_template('onboarding.html', jsonify(result=result),reader=reader,datas=datas, num=num,  columns=columns, dig=dig, all_cases_counter=all_cases_counter, Number_of_worflow=Number_of_worflow, form=form)

@app.route('/get_word')
def get_prediction():
    word = request.args.get('word')
    return jsonify({'prouductionforcast.html':getPrediction(word)})

@app.route('/onboarding/usecases')
def onboarding_showjson():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "static/data", "usecase.json")
    json_url2 = os.path.join(SITE_ROOT, "static/data", "columns.json")
    # csv to Json

    # json join to json
    #dictA = json.loads(json_url)
   # dictB = json.loads(json_url2)
    #merged_dict = {key: value for (key, value) in (dictA.items() + dictB.items())}
    # string dump of the merged dict
    #jsonString_merged = json.dumps(merged_dict)    
    #add to data
    data = json.load(open(json_url))
    columns =json.load(open(json_url2))
    




    return render_template('onboardingresults.html', data=data, columns = columns)



@app.route('/onboarding/api/v1.0/usecase', methods=['GET'])
def onboarding_get_usecases():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "static/data", "onboardingusecase.json")
    data = json.load(open(json_url))
    return jsonify({'data': data})
#read api per ID
@app.route('/onboarding/api/v1.0/usecase/<int:data_ID>', methods=['GET'])
def onboarding_get_usecase(data_ID):
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "static/data", "onboardingusecase.json")
    data = json.load(open(json_url))
    num  =int(data_ID)-1
    return jsonify({'data': data[num]})

# @app.route('/support/api/v1.0/usecase/profile/<int:data_ID>/', methods=['GET'])
# def get_usecaseprofile(data_ID):
#   SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
#   json_url = os.path.join(SITE_ROOT, "static/data", "usecase.json")
#   json_url2 = os.path.join(SITE_ROOT, "static/data", "columns.json")
#   data = json.load(open(json_url))
#   num  =int(data_ID)-1
#   columns =json.load(open(json_url2))
#   return render_template()

@app.route('/api')
def hello_world():
    return 'Hello, World!'

#@app.route('/api/devices' methods=['GET', 'POST'])
#def devices():

#tasks = [
#    {
#        'id': 1,
#        'title': u'Buy groceries',
#        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
#        'done': False
#    },
#    {
#        'id': 2,
#        'title': u'Learn Python',
#        'description': u'Need to find a good Python tutorial on the web', 
#        'done': False
#    }
#]

devices = [
    {
        'id':1,
        'title': u'EDA',
        'description': u'our discovry application that captures wire data',
        'done': False
    },
    {
        'id':2,
        'title': u'EXA',
        'description': u'our records application that captures records from devices',
        'done': False
    }

]
@app.route('/support/api/v1.0/devices', methods=['POST'])
def support_create_device():
    if not request.json or not 'title' in request.json:
        abort(400)
    device = {
        'id': devices[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    devices.append(device)
    return jsonify({'device': device}), 201

@app.route('/support/api/v1.0/devices<int:device_id>', methods=['GET'])
def support_get_device(device_id):
    device = [device for device in devices if device['id'] == device_id]
    if len(device) == 0:
        abort(404)
    return jsonify({'device': device[0]})

@app.route('/support/api/v1.0/devices', methods=['GET'])
def support_get_devices():
    return jsonify({'devices': devices})
#@app.route('/todo/api/v1.0/tasks', methods=['GET'])
#def get_tasks():
    #return jsonify({'tasks': tasks})



class VideoWorkflows(object):

    # Define some states. Most of the time, narcoleptic superheroes are just like
    # everyone else. Except for...
    states = ['input', 'Review1', 'Activity1', 'Review2', 'Activity2','Review3', 'Activity3' 'output']
    
    def __init__(self, name):

        # No anonymous superheroes on my watch! Every narcoleptic superhero gets
        # a name. Any name at all. SleepyMan. SlumberGirl. You get the idea.
        self.name = name

        # What have we accomplished today?
        self.points = 0
       
        # Initialize the state machine
        self.machine = Machine(model=self, states=VideoWorkflows.states, initial='input')
        
        # Add some transitions. We could also define these using a static list of
        # dictionaries, as we did with states above, and then pass the list to
        # the Machine initializer as the transitions= argument.

        # At some point, every superhero must rise and shine.
        self.machine.add_transition(trigger='start_work', source='input', dest='Review1')

        # Superheroes need to keep in shape.
        self.machine.add_transition('Read_docs', 'Review1', 'Activity1')

        # Those calories won't replenish themselves!
        self.machine.add_transition('Become_SME', 'Activity1', 'Write_Steps')

        # Superheroes are always on call. ALWAYS. But they're not always
        # dressed in work-appropriate clothing.
        self.machine.add_transition('technically_complate', 'Review2', 'All actions',
                         before='videotagraphy')

        # When they get off work, they're all sweaty and disgusting. But before
        # they do anything else, they have to meticulously log their latest
        # escapades. Because the legal department says so.
        self.machine.add_transition('stackholders_sign', 'Storyboard', 'powerpoint',
                         after='update_Player')
class videoTasks(object):  
    states= ['inputtasklist', 'Review1tasklist', 'Activity1tasklist']
    def __init__(self, name):
        # PoC: Initialize the 'task machine'
        self.machine= Machine(model=self, states=videoTasks.states, initial='inputtasklist')

        self.machine.add_transition(trigger='add_tasklist1', source='inputtasklist', dest='Review1tasklist') 
    
    
@app.route('/house1', methods=['GET', 'POST'])
def house1():
    VideoProduct = VideoWorkflows("VideoProduct")
    videoTask = videoTasks("videoTask")
    VideoProduct2 = VideoWorkflows("VideoProduct2")
    VideoProduct3 = VideoWorkflows("VideoProduct3")
    Users=mongo.db.users.find({})
    login_user = mongo.db.users.find_one({'name' : session['username']})
    i = Insightly()

    projects = i.read('tasks',id=8110743)
    print projects

    return render_template('house1.html', projects=projects, Users=Users, login_user=login_user,videoTask=videoTask, VideoProduct3=VideoProduct3,VideoProduct2=VideoProduct2, VideoProduct=VideoProduct)
@app.route('/notebooks', methods=['GET', 'POST'])
def notebooks():
    VideoProduct = VideoWorkflows("VideoProduct")
    videoTask = videoTasks("videoTask")
    VideoProduct2 = VideoWorkflows("VideoProduct2")
    VideoProduct3 = VideoWorkflows("VideoProduct3")
    Users=mongo.db.users.find({})
    login_user = mongo.db.users.find_one({'name' : session['username']})
    i = Insightly()
    projects = i.read('tasks')
    #print projects

    return render_template('notebook.html', projects=projects, Users=Users, login_user=login_user,videoTask=videoTask, VideoProduct3=VideoProduct3,VideoProduct2=VideoProduct2, VideoProduct=VideoProduct)

@app.route('/storypad/', methods=['GET', 'POST'])
def storypad():
    Users=mongo.db.users.find({})
    login_user = mongo.db.users.find_one({'name' : session['username']})
    Certs= mongo.db.certifications.find({})
    #print projects

    return render_template('notebookUI.html',Certs=Certs , Users=Users, login_user=login_user)

    
if __name__ == "__main__":
 
    app.debug = True
    app.secret_key = 'mysecret'
    app.run(port=5000)    
   
