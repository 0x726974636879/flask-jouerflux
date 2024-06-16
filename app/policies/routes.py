from flask import Blueprint, request, jsonify
from flasgger import swag_from

from app import db
from app.policies.decorators import validate_add_policy_request
from app.policies.models import Policy


policies = Blueprint("policies", __name__)


@policies.route("/policies", methods=["POST"])
@swag_from("swagger/add_policy.yml")
@validate_add_policy_request
def add_policy():
    """
    Endpoint to add a new a policy.
    """
    data = request.get_json()
    name = data.get("name")
    firewall_id = data.get("firewall_id")

    try:
        new_policy = Policy(name=name, firewall_id=firewall_id)
        db.session.add(new_policy)
        db.session.commit()

        response = jsonify(new_policy.to_dict()), 201
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({"message": "Server error"}), 500
    else:
        return response


@policies.route("/policies", methods=["GET"])
@swag_from("swagger/get_policies.yml")
def get_policies():
    """
    Endpoint to get all policies with pagination.
    """
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    if per_page > 10:
        per_page = 10

    pagination = Policy.query.paginate(
        page=page, per_page=per_page, error_out=False
    )
    policies = pagination.items

    response = {
        "items": [policy.to_dict() for policy in policies],
        "total_pages": pagination.pages,
        "current_page": page,
        "next_page": pagination.next_num if pagination.has_next else None,
        "prev_page": pagination.prev_num if pagination.has_prev else None,
    }
    return jsonify(response), 200


@policies.route("/policies/<int:id>", methods=["DELETE"])
@swag_from("swagger/delete_policy.yml")
def delete_policy(id):
    """
    Endpoint to delete a policy by ID.
    """
    policy = Policy.query.get(id)
    if policy is None:
        return jsonify({"message": f"Policy '{id}' not found"}), 404

    try:
        db.session.delete(policy)
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({"message": "Server error"}), 500
    else:
        return "", 200
