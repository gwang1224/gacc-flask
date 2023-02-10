from flask import Blueprint, request
from flask_restful import Api, Resource, reqparse
from .. import db
from ..model.todos import Todo

todo_bp = Blueprint("todos", __name__)
todo_api = Api(todo_bp)