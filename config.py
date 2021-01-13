import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
bd_report = Flask(__name__)
bd_report.config['SECRET_KEY'] = 'MyKey'

basedir = os.path.abspath(os.path.dirname(__file__))
bd_report.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data.sqlite')
bd_report.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

key = 'fb7f74a4c2a53d4ef8020c9890ad6411'

db = SQLAlchemy(bd_report)
migrate=Migrate(bd_report,db)
