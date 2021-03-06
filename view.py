import requests
import json
from flask import render_template, redirect, url_for,request,json,session
from sqlalchemy import extract
from model import Project,Designation,Task,User,TimeSheet
from forms import AddProject,ViewProject,ViewUser,ViewWork,AskDesignation, AddUser, AddWork
from config import db, bd_report, key
from middleware import Middleware
from datetime import datetime

#################### UPDATED TO CHECK PULL PUSH GIT ###############
############ Second Check ############
######### VIEW FUNCTIONS ##########

to_reload = False

@bd_report.route('/',methods=['GET','POST'])
def index():
    return render_template('trello_login.html')

@bd_report.route('/home')
def home():
    return render_template("home.html")

@bd_report.route('/token_post',methods=["GET",'POST'])
def token_post():
    res = {}
    if request.method == "POST" or request.method == "GET":
        token = request.form['token']
        base_url = 'https://trello.com/1/'
        mem_url = base_url + 'members/me'
        params_key_and_token = {'key': key, 'token': token}
        response = requests.get(mem_url, params=params_key_and_token)
        response = response.json()
        trello_id = response['id']
        user = response['username']
        session['token'] = token
        if trello_id == None:
            res['error'] = "/index"
        elif trello_id:
            get_user = User.query.filter_by(trello_id=trello_id).first()
            if get_user:
                res['success']='/add_project'
                token=token
                db.session.commit()
            else:
                res['trello_id']=trello_id
                res['user']=user
                token=token
                res['token']=token
                res['success'] ='/ask_designation'+'?'+'trello_id='+res['trello_id']+'&'+'user='+res['user']+'&'+'token='+res['token']

        res = json.dumps(res)
        return res


    return render_template('trello_login.html')

@bd_report.route('/ask_designation',methods=['GET','POST'])
def ask_designation():
    form = AskDesignation()
    if form.validate_on_submit():
        designation = form.designation.data
        designation_id = designation.id
        token = request.args.get('token')
        trello_id = request.args.get('trello_id')
        user = request.args.get('user')
        insert = User(trello_id,token,user,designation_id)
        db.session.add(insert)
        db.session.commit()

        session['token'] = token
        session['user'] = user
        session['trello_id'] = trello_id
        session['user_id'] = insert.id
        session['designation_id'] = designation_id
        return redirect(url_for('add_project'))
    return render_template('add/ask_designation.html',form=form)


@bd_report.route('/add_project',methods=['GET','POST'])
def add_project():
    form = AddProject()

    trello_id = session.get('trello_id')
    token = session.get('token')


    base_url = 'https://trello.com/1/'
    board_url = base_url+'members/{}/boards'.format(trello_id)

    params_key_and_token = {'key': key, 'token': token}

    response = requests.get(board_url, params=params_key_and_token)
    data = list(response.json())
    data_boards = {j['id']:j['name'] for j in data}

    if form.validate_on_submit():
        board_id = request.form.get("data_boards")
        project_name = request.form.get("board_name")

        list_id = request.form.get("data_list")
        list_name = request.form.get("list_name")

        card_id = request.form.get("data_card")
        card_name = request.form.get("card_name")

        date = request.form["date"]
        work = form.work.data
        hours = form.hours.data
        date = datetime.strptime(date,'%Y-%m-%d')

        work_id = work.id
        user_id = session.get('user_id')
        designation_id = session.get('designation_id')

        get_board_id = Project.query.filter_by(board_id=board_id).first()
        if get_board_id == None:
            add_board = Project(project_name,board_id)
            db.session.add(add_board)
            db.session.commit()
            project_id = add_board.id
        else:
            project_id = get_board_id.id
        add_data = TimeSheet(user_id,project_id,work_id,card_id,card_name,date,hours)
        db.session.add(add_data)
        db.session.commit()

        data = TimeSheet.query.order_by(TimeSheet.id.desc()).limit(10).all()

        return render_template('add/add_project.html',form=form,data=data,data_boards=data_boards)

    return render_template('add/add_project.html',form=form,data_boards=data_boards)

@bd_report.route('/add_user',methods=['GET','POST'])
def add_user():
    form = AddUser()
    if form.validate_on_submit():
        user = form.user.data
        designation = form.designation.data
        get_designation = Designation.query.filter_by(designation=designation).first()
        if get_designation == None:
            add_designation = Designation(designation)
            db.session.add(add_designation)
            db.session.commit()
            designation_id = add_designation.id
        else:
            designation_id = get_designation.id
        add_user = User(user, designation_id)
        db.session.add(add_user)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add/add_user.html',form=form)


@bd_report.route('/data_list',methods=['GET','POST'])
def data_list():
    board_id = request.form['board_id']
    token = session.get('token')

    base_url = 'https://trello.com/1/'
    list_url = base_url+"boards/{}/lists".format(board_id)

    params_key_and_token = {'key': key, 'token': token}
    response_list = requests.get(list_url,params=params_key_and_token)

    data = response_list.json()
    data_list = {j['id']: j['name'] for j in data}
    data_list = json.dumps(data_list)

    return data_list

@bd_report.route('/hello',methods=['GET','POST'])
def add_work():
    form = AddWork()
    if form.validate_on_submit():
        work = form.work.data
        designation = form.designation.data
        designation_id = designation.id
        add_work = Task(work,designation_id)
        db.session.add(add_work)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add/add_work.html',form=form)

@bd_report.route('/data_card',methods=['GET','POST'])
def data_card():
    list_id = request.form['list_id']
    token = session.get('token')


    base_url = 'https://trello.com/1/'
    card_url = base_url+"lists/{}/cards".format(list_id)

    params_key_and_token = {'key': key, 'token': token}
    response_card = requests.get(card_url, params=params_key_and_token)

    data = response_card.json()
    data_card = {j['id']: j['name'] for j in data}
    data_card = json.dumps(data_card)
    return data_card


@bd_report.route('/view_report',methods=['GET','POST'])
def view_project():
    form = ViewProject()
    if form.validate_on_submit():
        project_name = form.project_name.data
        date = request.form.get("date")
        date = datetime.strptime(date,'%Y-%m-%d')
        month = date.month
        user = session.get('user')
        data = TimeSheet.query.filter((extract('month',TimeSheet.date)==month),TimeSheet.project==project_name).all()
        work_view = Task.query.all()
        arr = {}
        for i in work_view:
            arr[i.id] = [j for j in data if j.work.designation_id == i.designation_id and j.task_id == i.id]
        return render_template("view/view_report.html",work_view=work_view,arr=arr)
    return render_template('view/view_project.html',form=form)

@bd_report.route('/view_user',methods=['GET','POST'])
def view_user():
    form = ViewUser()
    if form.validate_on_submit():
        user = form.user.data
        date = request.form.get("date")
        date = datetime.strptime(date,'%Y-%m-%d')
        month = date.month
        data = TimeSheet.query.filter(extract("month",TimeSheet.date)==month,TimeSheet.user==user).all()
        return render_template("view/view_report_user.html",data=data)
    return render_template('view/view_user.html', form=form)

@bd_report.route('/view_work',methods=['GET','POST'])
def view_work():
    form = ViewWork()
    if form.validate_on_submit():
        work = form.work.data
        date = request.form.get("date")
        date = datetime.strptime(date,'%Y-%m-%d')
        month = date.month
        data = TimeSheet.query.filter(extract("month",TimeSheet.date)==month,TimeSheet.work==work).all()
        return render_template("view/view_report_work.html",data=data)
    return render_template("view/view_work.html",form=form)

if __name__ == '__main__':
    bd_report.run(debug=True)
