# coding = utf-8
from . import home
from flask import render_template, redirect, url_for


# redirect 退出
# url_for 路由生成器


@home.route('/')
def index():
    return render_template("home/index.html")


@home.route('/login/')
def login():
    return render_template("home/login.html")



@home.route('/logout/')
def logout():
    return redirect(url_for("home.login"))

@home.route('/register/')
def register():
    return  render_template("home/register.html")

@home.route('/user/')
def user():
    return  render_template("home/user.html")