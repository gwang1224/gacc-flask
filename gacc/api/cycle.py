from flask import Blueprint, jsonify  # jsonify creates an endpoint response object
from flask_restful import Api, Resource # used for REST API building
import requests
from ... import db
from ..model.cycle import Cycle

cycle_bp = Blueprint("cycle", __name__)
cycle_api = Api(cycle_bp)

class CycleAPI(Resource):
    def get(self):
        id = request.args.get("id")
        cycle = db.session.query(Cycle).get(id)
        if cycle:
            return cycle.to_dict()
        return {"message": "cycle not found"}, 404

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("lastperiod", required=True, type=str)
        parser.add_argument("periodlength", required=True, type=int)
        parser.add_argument("cyclelength", required=True, type=int)
        
        args = parser.parse_args()
        
        cycle = Cycle(args["lastperiod"], args["periodlength"], args["cyclelength"], args["endTime"])
        try:
            db.session.add(cycle)
            db.session.commit()
            return cycle.to_dict(), 201
        except Exception as e:
            db.session.rollback()
            return {"message": f"server error: {e}"}, 500
    
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument("id", required=True, type=int)
        args = parser.parse_args()

        try:
            todo = db.session.query(Cycle).get(args["id"])
            if todo:
                todo.completed = args["completed"]
                db.session.commit()
                return cycle.to_dict()
            else:
                return {"message": "cycle not found"}, 404
        except Exception as e:
            db.session.rollback()
            return {"message": f"server error: {e}"}, 500

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument("id", required=True, type=int)
        args = parser.parse_args()

        try:
            todo = db.session.query(Cycle).get(args["id"])
            if todo:
                db.session.delete(cycle)
                db.session.commit()
                return cycle.to_dict()
            else:
                return {"message": "cycle not found"}, 404
        except Exception as e:
            db.session.rollback()
            return {"message": f"server error: {e}"}, 500

class TodoListAPI(Resource):
    def get(self):
        todos = db.session.query(Cycle).all()
        return [cycle.to_dict() for cycle in cycles]

cycle_api.add_resource(CycleAPI, "/todo")
cycle_api.add_resource(CycleListAPI, "/cycleList")
