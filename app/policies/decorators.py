from functools import wraps

from flask import request, jsonify

from app.firewalls.models import Firewall
from app.policies.models import Policy


def validate_add_policy_request(func):
    """
    Decorator to validate the request data for adding a new policy.

    Returns
    -------
    _: func
        Wrapped function if all validations pass, otherwise returns a JSON
        response with an appropriate error message and HTTP status code.

        - 400: If 'name' or 'firewall_id' is missing or if 'name'
               exceeds 50 characters.
        - 409: If a policy with the same name already exists for
               the given 'firewall_id'.
        - 404: If the specified 'firewall_id' does not exist.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        data = request.get_json()
        name = data.get("name")
        firewall_id = data.get("firewall_id")

        if not name:
            return jsonify({"message": "Parameter 'name' required"}), 400

        if not firewall_id:
            return jsonify(
                {"message": "Parameter 'firewall_id' required"}
            ), 400

        if len(name) > 50:
            return jsonify(
                {"message": "Parameter 'name' must be 50 characters maximum"}
            ), 400

        firewall = Firewall.query.get(firewall_id)

        if not firewall:
            return jsonify(
                {"message": f"Firewall '{firewall_id}' doesn't exist"}
            ), 404

        if Policy.query.filter_by(name=name, firewall_id=firewall_id).first():
            return jsonify({
                "message": (
                    f"Policy name '{name}' already exists for "
                    f"'{firewall.name}'"
                )
            }), 409

        return func(*args, **kwargs)
    return wrapper
