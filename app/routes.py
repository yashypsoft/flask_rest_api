# app/routes.py

from flask import Blueprint, jsonify, request
from .models import Query, Address, db
import os
import time
import socket
from sqlalchemy.exc import SQLAlchemyError

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET'])
def query_status():
    response = {
        "version": "0.1.0",
        "date": int(time.time()),
        "kubernetes": os.getenv("KUBERNETES_SERVICE_HOST") is not None
    }
    return jsonify(response), 200

@main_bp.route('/health', methods=['GET'])
def query_health():
    return jsonify({"status": "healthy"}), 200

@main_bp.route('/v1/tools/lookup', methods=['GET'])
def lookup_domain():
    domain = request.args.get('domain')
    if not domain:
        return jsonify({"message": "Domain name is required"}), 400

    try:
        ipv4_addresses = socket.gethostbyname_ex(domain)[2]
        client_ip = request.remote_addr
        
        query = Query(domain=domain, client_ip=client_ip)
        db.session.add(query)
        db.session.commit()

        for ip in ipv4_addresses:
            address = Address(ip=ip, query_id=query.id)
            db.session.add(address)

        db.session.commit()
        
        return jsonify({
            "domain": domain,
            "client_ip": client_ip,
            "addresses": ipv4_addresses
        }), 200

    except socket.gaierror:
        return jsonify({"message": "Domain not found"}), 404
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500

@main_bp.route('/v1/tools/validate', methods=['POST'])
def validate_ip():
    data = request.get_json()
    ip = data.get('ip')

    try:
        socket.inet_aton(ip)
        return jsonify({"status": True}), 200
    except socket.error:
        return jsonify({"status": False}), 200

@main_bp.route('/v1/history', methods=['GET'])
def queries_history():
    try:
        queries = Query.query.order_by(Query.id.desc()).limit(20).all()
        history = [
            {
                "queryID": query.id,
                "domain": query.domain,
                "client_ip": query.client_ip,
                "created_time": query.created_time,
                "addresses": [addr.ip for addr in query.addresses]
            }
            for query in queries
        ]
        return jsonify(history), 200
    except SQLAlchemyError as e:
        return jsonify({"message": str(e)}), 500
