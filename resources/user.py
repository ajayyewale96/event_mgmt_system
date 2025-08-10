from flask_smorest import Blueprint,abort
from flask.views import MethodView
from sqlalchemy.exc import IntegrityError,SQLAlchemyError
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token
from schemas import UserSchema
from models import UserModel
from db import db
blp=Blueprint('Users',__name__,'operation on users')

@blp.route('/register')
class UserRegistration(MethodView):
    @blp.arguments(UserSchema)
    @blp.response(201,UserSchema)
    def post(self,user):
        new_user=UserModel(username=user['username'],
                           password=pbkdf2_sha256.hash(user['password']))
        try:
            db.session.add(new_user)
            db.session.commit()
        except IntegrityError:
            abort(400,message='User already exists')
        except SQLAlchemyError as e:
            abort(500,message='Error occured while registering the user')
        except Exception as e:
            abort(500,message=f'{e}')
        return new_user

@blp.route('/login')
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self,user):
        existing_user=UserModel.query.filter(UserModel.username==user['username']).first_or_404()
        if pbkdf2_sha256.verify(user['password'],existing_user.password):
            access_token=create_access_token(identity=str(existing_user.id))
            return {'access_token':access_token},200    
        abort(400,message='Incorrect password')