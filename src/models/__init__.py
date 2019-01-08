from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

# initialize our db
db = SQLAlchemy()
bcrypt = Bcrypt()

from .QuestionModel import QuestionModel
from .QuestionModel import  QuestionSchema
from .UserModel import UserModel
from .UserModel import UserSchema
