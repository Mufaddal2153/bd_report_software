import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
bd_report = Flask(__name__)
bd_report.config['SECRET_KEY'] = 'MyKey'

basedir = os.path.abspath(os.path.dirname(__file__))
bd_report.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data.sqlite')
bd_report.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(bd_report)