from flask import jsonify
from flask_cors import cross_origin
from flask_restplus import Resource, cors

from app.main.adapter.todo_dao import TodoDAO
from app.main.model.todo_dto import TodoDTO
from app.main.util.auth_decorator import token_required

api = TodoDTO.api

_todo = TodoDTO.todo

DAO = TodoDAO(api)
DAO.create({"task": "Build an API"})
DAO.create({"task": "?????"})
DAO.create({"task": "profit!"})
DAO.create({"task": "New Task!"})


@cors.crossdomain(origin="*")
@api.route("/")
class TodoList(Resource):
    """Shows a list of all todos, and lets you POST to add new tasks"""

    @api.doc("list_todos")
    @api.marshal_list_with(_todo)
    def get(self):
        """List all tasks"""
        return DAO.todos

    @api.doc("create_todo")
    @api.expect(_todo, validate=True)
    @token_required
    @api.marshal_with(_todo, code=201)
    @api.response(201, "Todo successfully created.")
    def post(self):
        """Create a new task"""
        return DAO.create(api.payload), 201


@cors.crossdomain(origin="*")
@api.route("/<int:id>")
@api.response(404, "Todo not found")
@api.param("id", "The task identifier")
class Todo(Resource):
    """Show a single todo item and lets you delete them"""

    @api.doc("get_todo")
    @api.marshal_with(_todo)
    def get(self, id):
        """Fetch a given resource"""
        return DAO.get(id)

    @api.doc("delete_todo")
    @api.response(204, "Todo deleted")
    def delete(self, id):
        """Delete a task given its identifier"""
        DAO.delete(id)
        return "", 204

    @api.doc("update_todo")
    @api.expect(_todo, validate=True)
    @api.marshal_with(_todo)
    def put(self, id):
        """Update a task given its identifier"""
        return DAO.update(id, api.payload)
