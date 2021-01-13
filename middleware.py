from werkzeug.wrappers import Request, Response, ResponseStream
from model import Project,Designation,Task,User,TimeSheet
from flask import session,redirect,url_for
from config import db, bd_report

class Middleware():
    def __init__(self,bd_report):
        self.bd_report = bd_report
    def __call__(self):
        token = session.get('token')
        if token==None:
            return redirect(url_for("token_post"))
        else:
            return