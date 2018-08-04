# coding = utf-8
from flask import  Flask

app = Flask(__name__)
app.debug = True    #todo 部署到服务器是设置为False
from app.home import home as home_blueprint
from app.admin import admin as admin_blueprint

app.register_blueprint(home_blueprint)
app.register_blueprint(admin_blueprint,url_prefix='/admin')
