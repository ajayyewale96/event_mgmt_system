from flask import Flask
from flask_smorest import Api,abort
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
import os
from time import sleep
import models
from resources.event import blp as EventBluePrint
from resources.user import blp as UserBluePrint
from db import db


def create_app(db_url=None):
    app=Flask(__name__)
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Event Management REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config['JWT_SECRET_KEY']=os.getenv('JWT_SECRET_KEY','secret')

    jwt=JWTManager(app)
    
    @jwt.expired_token_loader
    def expired_token_loader_callback(jwt_header,jwt_payload):
        return {
            'message':'Token has expired',
            'error':'expired_token'
        },401
    
    @jwt.additional_claims_loader
    def additional_claims_loader_callback(identity):
        if identity==1:
            return {'is_admin':True}
        return {'is_admin':False}
    
    @jwt.invalid_token_loader
    def invalid_token_loader_callback(error):
        return {
            'message':'JWT is invalid',
            'error':error
        },401
    
    @jwt.needs_fresh_token_loader
    def needs_fresh_token_loader(jwt_header,jwt_payload):
        return {
            'message':'need a fresh token',
            'error':'fresh_token_required'
        },401
    
    @jwt.revoked_token_loader
    def revoked_token_loader_callback(wt_header,jwt_payload):
        return {
            'message':'Blocked token is used',
            'error':'revoked_token_provided'
        },401
    
    @jwt.unauthorized_loader
    def unauthorized_loader_callback(error):
        return {
            'message':'Request does not contain acccess token',
            'error':error
        },401
    
    Migrate(app,db)
    db.init_app(app)
    
    api=Api(app)
 
    api.register_blueprint(EventBluePrint)
    api.register_blueprint(UserBluePrint)

    return app

    