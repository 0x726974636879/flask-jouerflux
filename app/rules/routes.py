from flask import Blueprint, jsonify, request
from flasgger import swag_from

from app import db
from app.rules.decorators import validate_add_rule_request
from app.rules.models import Rule


rules = Blueprint("rules", __name__)


@rules.route("/rules", methods=["POST"])
@swag_from("swagger/add_rule.yml")
@validate_add_rule_request
def add_rule():
    """
    Endpoint to add a new rule.
    """
    data = request.get_json()
    name = data.get("name")
    policy_id = data.get("policy_id")

    try:
        new_rule = Rule(name=name, policy_id=policy_id)
        db.session.add(new_rule)
        db.session.commit()

        response = jsonify(new_rule.to_dict()), 201
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({"message": "Server error"}), 500
    else:
        return response


@rules.route("/rules", methods=["GET"])
@swag_from("swagger/get_rules.yml")
def get_rules():
    """
    Endpoint to get all rules with pagination.
    """
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    if per_page > 10:
        per_page = 10

    pagination = Rule.query.paginate(
        page=page, per_page=per_page, error_out=False
    )
    rules = pagination.items

    response = {
        "items": [rule.to_dict() for rule in rules],
        "total_pages": pagination.pages,
        "current_page": page,
        "next_page": pagination.next_num if pagination.has_next else None,
        "prev_page": pagination.prev_num if pagination.has_prev else None,
    }
    return jsonify(response), 200


@rules.route("/rules/<int:id>", methods=["DELETE"])
@swag_from("swagger/delete_rule.yml")
def delete_rules(id):
    """
    Endpoint to delete a rule by ID.
    """
    rule = Rule.query.get(id)
    if rule is None:
        return jsonify({"message": f"Rule {id} not found"}), 404

    try:
        db.session.delete(rule)
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({"message": "Server error"}), 500
    else:
        return "", 200
