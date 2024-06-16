from functools import wraps

from flask import request, jsonify

from app.firewalls.models import Firewall


def validate_add_firewall_request(func):
    """
    Decorator to validate the request data for adding a new firewall.

    Returns
    -------
    _: func
        Wrapped function if all validations pass, otherwise returns a JSON
        response with an appropriate error message and HTTP status code.

        - 400: If 'name' is missing or if 'name' exceeds 50 characters.
        - 409: If a firewall with the same name already exists.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        data = request.get_json()
        name = data.get("name")

        if not name:
            return jsonify({"message": "Parameter 'name' is required"}), 400

        if len(name) > 50:
            return jsonify(
                {"message": "Parameter 'name' must be 50 characters maximum"}
            ), 400

        if Firewall.query.filter_by(name=name).first():
            return jsonify({
                "message": f"A firewall with the name '{name}' already exists"
            }), 409

        return func(*args, **kwargs)
    return wrapper
