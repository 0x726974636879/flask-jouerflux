from functools import wraps

from flask import request, jsonify

from app.policies.models import Policy
from app.rules.models import Rule


def validate_add_rule_request(func):
    """
    Decorator to validate the request data for adding a new rule.

    Returns
    -------
    _: func
        Wrapped function if all validations pass, otherwise returns a JSON
        response with an appropriate error message and HTTP status code.

        - 400: If 'name' or 'policy_id' is missing or if 'name'
                exceeds 50 characters.
        - 409: If a rule with the same name already exists for
                the given 'policy_id'.
        - 404: If the specified 'policy_id' does not exist.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        data = request.get_json()
        name = data.get("name")
        policy_id = data.get("policy_id")

        if not name:
            return jsonify({"message": "Parameter 'name' is required"}), 400

        if not policy_id:
            return jsonify(
                {"message": "Paramter 'policy_id' is required"}
            ), 400

        if len(name) > 50:
            return jsonify(
                {"message": "Name must be 50 characters maximum"}
            ), 400

        policy = Policy.query.get(policy_id)

        if not policy:
            return jsonify(
                {"message": f"Policy '{policy_id}' doesn't exist"}
            ), 404

        if Rule.query.filter_by(name=name, policy_id=policy.id).first():
            return jsonify(
                {
                    "message": (
                        f"A rule with the name '{name}' already "
                        f"exists for '{policy.id}'"
                    )
                }
            ), 409

        return func(*args, **kwargs)
    return wrapper
