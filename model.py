from config import db, bd_report,migrate
from sqlalchemy.orm import backref

####### Models ########

class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer,primary_key = True)
    board_id = db.Column(db.Integer)
    project_name = db.Column(db.Text)

    #project_ts = db.relationship('TimeSheet',backref='project')
    #customer = db.Column(db.Text)

    def __init__(self,project_name,board_id):
        self.project_name = project_name
        self.board_id = board_id
     #   self.customer = customer
    def __repr__(self):
        pass

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key=True)
    trello_id = db.Column(db.Integer)
    user = db.Column(db.Text)
    token = db.Column(db.String(300))
    
    #user_ts = db.relationship('TimeSheet',backref='user')

    designation_id = db.Column(db.Integer,db.ForeignKey('designations.id'))
    designation = db.relationship("Designation", backref=backref("users"))

    def __init__(self,trello_id,token,user, designation_id):
        self.trello_id = trello_id
        self.token = token
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
    date = db.Column(db.Date)

    project_id = db.Column(db.Integer,db.ForeignKey('projects.id'))
    project = db.relationship("Project",backref=backref("TimeSheet"))

    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    user = db.relationship("User",backref=backref("TimeSheet"))

    hours = db.Column(db.Float)

    task_id = db.Column(db.Integer,db.ForeignKey('tasks.id'))
    work = db.relationship("Task",backref=backref("TimeSheet"))

    card_id = db.Column(db.Integer)
    card_name = db.Column(db.Text)

    def __init__(self,user_id,project_id,task_id,card_id,card_name,date,hours):
        self.user_id = user_id
        self.project_id = project_id
        self.task_id = task_id
        self.card_id = card_id
        self.card_name = card_name
        self.date = date
        self.hours = hours
    def __repr__(self):
        pass
db.create_all()
