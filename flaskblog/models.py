from datetime import datetime
from flaskblog import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
#    __tablename__='user'
    id=db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
#    posts = db.relationship('Post',backref='author', lazy=True)

    def __repr__(self):
        return "User('{}', '{}', '{}')".format(self.username,self.email,self.image_file)
#posts=[{'author':'Ajay Singh','title':'Blog Post 1','date_posted':'12/01/2018','content':'This is Ajay hello'},{'author':'Archana singh','title':'Blog post 2','date_posted':'12/01/2018','content':'This is Archana hello'}]

# class Post(db.Model):
# #    __tablename__='post'
#     id=db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(100), nullable=False )
#     date_posted = db.Column(db.DateTime,  nullable=False, default=datetime.utcnow)
#     content = db.Column(db.Text, nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
#
#     def __repr__(self):
#         return "Post('{}', '{}')".format(self.title,self.date_posted)

class Inv_Content(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    machine_name = db.Column(db.String(20), unique=True, nullable=False)
    in_date = db.Column(db.DateTime,  nullable=False, default=datetime.utcnow)
    model = db.Column(db.String(60), nullable=False)
    location = db.Column(db.String(60), nullable=False)
    def __repr__(self):
        return "Inv_Content('{}', '{}', '{}', '{}')".format(self.machine_name,self.in_date,self.model,self.location)
