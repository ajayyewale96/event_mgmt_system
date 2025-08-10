from flask import Flask
from flask_smorest import Api,abort
from sqlalchemy.exc import SQLAlchemyError
import os
from time import sleep
import models
from resources.event import blp as EventBluePrint
from db import db


def create_app(db_url='postgresql+psycopg2://postgres:postgres@postgres/event_mgmt_system'):
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
    db.init_app(app)
    api=Api(app)
    db_connection_retry=5
    with app.app_context():
        while db_connection_retry > 0:
            try:
                db.create_all()
                break
            except SQLAlchemyError:
                sleep(60//db_connection_retry)
                db_connection_retry-=1
                
        if db_connection_retry <=0:
            abort(500,message='Error occured while connecting the db')
            
    api.register_blueprint(EventBluePrint)

    return app

    