from flask import Blueprint, request, jsonify
from flasgger import swag_from

from app import db
from app.firewalls.decorators import validate_add_firewall_request
from app.firewalls.models import Firewall
from app.policies.models import Policy
from app.rules.models import Rule


firewalls = Blueprint("firewalls", __name__)


@firewalls.route("/firewalls", methods=["POST"])
@swag_from("swagger/add_firewall.yml")
@validate_add_firewall_request
def add_firewall():
    """
    Endpoint to add a new firewall.
    """
    data = request.get_json()
    name = data.get("name")

    try:
        new_firewall = Firewall(name=name)
        db.session.add(new_firewall)
        db.session.commit()

        response = jsonify(new_firewall.to_dict()), 201
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({"message": "Server error"}), 500
    else:
        return response


@firewalls.route("/firewalls/<int:id>", methods=["GET"])
@swag_from("swagger/get_firewall.yml")
def get_firewall(id):
    """
    Endpoint to get a firewall by ID
    """
    firewall = Firewall.query.get(id)
    if firewall is None:
        return jsonify({"message": f"Firewall '{id}' not found"}), 404

    policies = Policy.query.filter_by(firewall_id=id).all()
    policies_data = []
    for policy in policies:
        policy_data = policy.to_dict()
        rules = Rule.query.filter_by(policy_id=policy.id).all()
        policy_data["rules"] = [rule.to_dict() for rule in rules]
        policies_data.append(policy_data)

    firewall_data = firewall.to_dict()
    firewall_data["policies"] = policies_data

    return jsonify(firewall_data), 200


@firewalls.route("/firewalls", methods=["GET"])
@swag_from("swagger/get_all_firewalls.yml")
def get_all_firewalls():
    """
    Endpoint to get all firewalls with pagination.
    """
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    if per_page > 10:
        per_page = 10

    pagination = Firewall.query.paginate(
        page=page, per_page=per_page, error_out=False
    )
    firewalls = pagination.items

    response = {
        "items": [firewall.to_dict() for firewall in firewalls],
        "total_pages": pagination.pages,
        "current_page": page,
        "next_page": pagination.next_num if pagination.has_next else None,
        "prev_page": pagination.prev_num if pagination.has_prev else None,
    }
    return jsonify(response), 200


@firewalls.route("/firewalls/<int:id>", methods=["DELETE"])
@swag_from("swagger/delete_firewall.yml")
def delete_firewall(id):
    """
    Endpoint to delete a firewall by ID.
    """
    firewall = Firewall.query.get(id)
    if firewall is None:
        return jsonify({"message": f"Firewall '{id}' not found"}), 404

    try:
        db.session.delete(firewall)
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({"message": "Server error"}), 500
    else:
        return "", 200
