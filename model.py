from config import db, bd_report
from sqlalchemy.orm import backref

####### Models ########

class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer,primary_key = True)
    project_name = db.Column(db.Text)

    #project_ts = db.relationship('TimeSheet',backref='project')
    #customer = db.Column(db.Text)

    def __init__(self,project_name):
        self.project_name = project_name
     #   self.customer = customer
    def __repr__(self):
        pass

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key=True)
    user = db.Column(db.Text)

    #user_ts = db.relationship('TimeSheet',backref='user')

    designation_id = db.Column(db.Integer,db.ForeignKey('designations.id'))
    designation = db.relationship("Designation", backref=backref("users"))

    def __init__(self,user, designation_id):
        self.user = user
        self.designation_id = designation_id
    def __repr__(self):
        pass

class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer,primary_key=True)
    work = db.Column(db.Text)

    #task_ts = db.relationship('TimeSheet',backref='task')
    designation_id = db.Column(db.Integer,db.ForeignKey('designations.id'))
    designation = db.relationship("Designation", backref=backref("tasks"))

    def __init__(self,work,designation_id):
        self.work = work
        self.designation_id = designation_id
    def __repr__(self):
        pass

class Designation(db.Model):
    __tablename__ = 'designations'
    id = db.Column(db.Integer,primary_key=True)
    designation = db.Column(db.Text)
    #designation_users = db.relationship('User',backref='designation')
    #designation_work = db.relationship('Task',backref='designation')

    def __init__(self,designation):
        self.designation = designation

    def __repr__(self):
        pass
    def get_id(self):
        return self.id


class TimeSheet(db.Model):
    __tablename__ = 'timesheets'

    id = db.Column(db.Integer,primary_key = True)
    month = db.Column(db.Integer)

    month_data = {1: "January", 2: "Febuary", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July",
                  8: "August", 9: "September", 10: "October", 11: "November", 12: "December"}

    project_id = db.Column(db.Integer,db.ForeignKey('projects.id'))
    project = db.relationship("Project",backref=backref("TimeSheet"))

    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    user = db.relationship("User",backref=backref("TimeSheet"))

    hours = db.Column(db.Float)

    task_id = db.Column(db.Integer,db.ForeignKey('tasks.id'))
    work = db.relationship("Task",backref=backref("TimeSheet"))

    title = db.Column(db.Text)

    def __init__(self,month, project_id,user_id,hours,task_id,title):
        self.month = month
        self.project_id = project_id
        self.user_id = user_id
        self.hours = hours
        self.task_id = task_id
        self.title = title
    def __repr__(self):
        pass

db.create_all()