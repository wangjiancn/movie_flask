# !/usr/bin/python3
# coding = utf-8
import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:py123@localhost:3306/movie" #+pymysql调用pymysql
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 用户名
    pwd = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    phone = db.Column(db.String(11), unique=True)
    info = db.Column(db.Text)  # 个性简介
    face = db.Column(db.String(255), unique=True)  # 头像
    addtime = db.Column(db.DateTime, index=True, default=datetime.datetime.now)  # 注册时间
    uuid = db.Column(db.String(255), unique=True)  # 唯一标识符
    userlogs = db.relationship('Userlog', backref='user')  # 会员日志外键关联
    comments = db.relationship('Comment', backref='user')
    moviecols = db.relationship('Moviecol', backref='user')

    def __repr__(self):
        return "<User %r>" % self.name


# 会员登录日志
class Userlog(db.Model):
    __tablename__ = "userlog"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属会员,ForeignKey 关联表‘user’的‘id’字段
    ip = db.Column(db.String(100))
    addtiem = db.Column(db.DateTime, index=True, default=datetime.datetime.now)

    def __repr__(self):
        return "<Userlog %r>" % self.id


# 电影标签
class Tag(db.Model):
    __tablename__ = "tag"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 标题
    addtime = db.Column(db.DateTime, index=True, default=datetime.datetime.now)  # 添加时间
    movies = db.relationship("Movie", backref='tag')  # 电影外键关联

    def __repr__(self):
        return "<Tag %r>" % self.name


# 电影
class Movie(db.Model):
    __tablename__ = "movie"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    title = db.Column(db.String(255), unique=True)
    url = db.Column(db.String(255), unique=True)
    info = db.Column(db.Text)  # 简介
    logo = db.Column(db.String(255), unique=True)  # 封面
    star = db.Column(db.SmallInteger)  # 星级
    playnum = db.Column(db.BigInteger)  # 播放量
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))  # 所属标签
    area = db.Column(db.String(255))
    release_time = db.Column(db.Date)  # 播放时间
    length = db.Column(db.String(100))
    addtime = db.Column(db.DateTime, index=True, default=datetime.datetime.now)  # 添加时间
    comments = db.relationship('Comment', backref='movie')
    moviecols = db.relationship('Moviecol', backref='movie')

    def __repr__(self):
        return "<Movie %r>" % self.title


# 上映预告
class Preview(db.Model):
    __tablename__ = 'preview'
    id = db.Column(db.Integer, primary_key=True)  # 编号
    title = db.Column(db.String(255), unique=True)
    logo = db.Column(db.String(255), unique=True)  # 封面
    addtime = db.Column(db.DateTime, index=True, default=datetime.datetime.now)  # 添加时间

    def __repr__(self):
        return "<Preview %r>" % self.title


# 评论
class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)  # 编号
    content = db.Column(db.Text)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))  # 所属标签
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属标签
    addtime = db.Column(db.DateTime, index=True, default=datetime.datetime.now)  # 添加时间

    def __repr__(self):
        return '<Comment %r>' % self.title


# 收藏
class Moviecol(db.Model):
    __tablename__ = 'moviecol'
    id = db.Column(db.Integer, primary_key=True)  # 编号
    content = db.Column(db.Text)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))  # 所属标签
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属标签
    addtime = db.Column(db.DateTime, index=True, default=datetime.datetime.now)  # 添加时间

    def __repr__(self):
        return '<Moviecol %r>' % self.id


# 权限
class Auth(db.Model):
    __tablename__ = 'auth'
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)
    url = db.Column(db.String(255), unique=True)
    addtime = db.Column(db.DateTime, index=True, default=datetime.datetime.now)  # 添加时间

    def __repr__(self):
        return '<Auth %r>' % self.name


# 角色
class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)
    auths = db.Column(db.String(600), unique=True)
    addtime = db.Column(db.DateTime, index=True, default=datetime.datetime.now)  # 添加时间

    def __repr__(self):
        return '<Role %r>' % self.name


# 管理员
class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 用户名
    pwd = db.Column(db.String(100))
    is_super = db.Column(db.SmallInteger)#
    role_id = db.Column(db.Integer,db.ForeignKey('role.id'))#todo
    addtime = db.Column(db.DateTime, index=True, default=datetime.datetime.now)  # 添加时间
    adminlogs = db.relationship('Adminlog', backref='admin')
    oplogs = db.relationship('Oplog', backref='admin')


    def __repr__(self):
        return "<Admin %r>" % self.name



#管理员登陆日志
class Adminlog(db.Model):
    __tablename__ = "adminlog"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    user_id = db.Column(db.Integer, db.ForeignKey('admin.id'))  # 所属会员,ForeignKey 关联表‘user’的‘id’字段
    ip = db.Column(db.String(100))
    addtiem = db.Column(db.DateTime, index=True, default=datetime.datetime.now)

    def __repr__(self):
        return "<Adminlog %r>" % self.id

#后台操作日志
class Oplog(db.Model):
    __tablename__ = "oplog"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    user_id = db.Column(db.Integer, db.ForeignKey('admin.id'))  # 所属会员,ForeignKey 关联表‘user’的‘id’字段
    ip = db.Column(db.String(100))
    addtiem = db.Column(db.DateTime, index=True, default=datetime.datetime.now)

    def __repr__(self):
        return "<Oplog %r>" % self.id

if __name__ == '__main__':
    # db.create_all()#生产数据表
    # role = Role(
    #     name='管理员1',
    #     auths=''
    # )
    # db.session.add(role)
    # db.session.commit()

    admin = Admin(
        name= 'wj',
        pwd='11223344',
        is_super=1,
        role_id=1
    )
    db.session.add(admin)
    db.session.commit()