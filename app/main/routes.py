from flask import Blueprint, jsonify

main = Blueprint("main", __name__)


@main.route("/")
def index():
    """
    Endpoint returning hello world
    ---
    responses:
      200:
        description: Hello world
        schema:
          type: object
          properties:
            message:
              type: string
              example: hello world
    """
    return jsonify({"message": "hello world"}), 200
