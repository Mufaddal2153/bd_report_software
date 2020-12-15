import os
from flask import Flask, render_template, redirect, url_for,request

from flask_migrate import Migrate
from model import Project,Designation,Task,User,TimeSheet
from forms import AddProject,AddProjectName,AddUser,AddWork,ViewProject,ViewUser,ViewWork
from config import db, bd_report

######### VIEW FUNCTIONS ##########

@bd_report.route('/')
def index():
    return render_template('home.html')

@bd_report.route('/add_project',methods=['GET','POST'])
def add_project():
    form = AddProject()
    if form.validate_on_submit():
        user = form.user.data
        title = form.title.data
        hours = form.hours.data
        work = form.work.data
        month = request.form.get("month")
        project_name = form.project_name.data
        user_id = user.id
        work_id = work.id
        project_name_id = project_name.id
        report = TimeSheet(month, project_name_id, user_id, hours, work_id, title)
        db.session.add(report)
        db.session.commit()

        return redirect(url_for('add_project'))
    return render_template('add/add_project.html',form=form,month_data=TimeSheet.month_data)

@bd_report.route('/add_project_name',methods=['GET','POST'])
def add_project_name():
    form = AddProjectName()
    if form.validate_on_submit():
        project_name = form.project_name.data
        add_project = Project(project_name)
        db.session.add(add_project)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add/add_project_name.html',form=form)

@bd_report.route('/add_user',methods=['Get','POST'])
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

@bd_report.route('/add_work',methods=['GET','POST'])
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

@bd_report.route('/view_report',methods=['GET','POST'])
def view_project():
    form = ViewProject()
    if form.validate_on_submit():
        project_name = form.project_name.data
        month = request.form.get("month")
        timesheet = TimeSheet.query.filter_by(project=project_name,month=month).all()
        work_view = Task.query.all()
        arr = {}
        for i in work_view:
            arr[i.id]=[j for j in timesheet if j.work.designation_id==i.designation_id and j.task_id==i.id]

        return render_template("view/view_report.html",work_view=Task.query.all(),arr=arr)
    return render_template('view/view_project.html',form=form,month_data=TimeSheet.month_data)

@bd_report.route('/view_user',methods=['GET','POST'])
def view_user():
    form = ViewUser()
    if form.validate_on_submit():
        user = form.user.data
        month = request.form.get("month")
        timesheet = TimeSheet.query.filter_by(user=user, month=month).all()
        return render_template("view/view_report_user.html",data=timesheet)
    return render_template('view/view_user.html', form=form, month_data=TimeSheet.month_data)

@bd_report.route('/view_work',methods=['GET','POST'])
def view_work():
    form = ViewWork()
    if form.validate_on_submit():
        work = form.work.data
        month = request.form.get("month")
        timesheet = TimeSheet.query.filter_by(work=work,month=month).all()
        return render_template("view/view_report_work.html",data=timesheet)
    return render_template("view/view_work.html",form=form,month_data=TimeSheet.month_data)

if __name__ == '__main__':
    bd_report.run(debug=True)