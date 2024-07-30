from flask import Blueprint, jsonify
from flask_restful import Api, Resource, reqparse
from models import User, db
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, JWTManager, create_refresh_token, jwt_required, current_user
from functools import wraps


bcrypt = Bcrypt()
jwt = JWTManager()