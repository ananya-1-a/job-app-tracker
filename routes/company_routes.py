from flask import Blueprint,request,jsonify
from extensions import db
from models.company import Company
from flask_jwt_extended import jwt_required 

company_bp=Blueprint('companies',__name__)
@company_bp.route('/companies',methods=['POST'])
@jwt_required()
def add_company():
    data=request.get_json('name')
    if not data.get('name'):
        return jsonify({"error: company name is required"})
    new_company=Company(
        name=data.get('name'),
        location=data.get('location'),
        website=data.get('website'),
    )
    db.session.add(new_company)
    db.session.commit()

    return jsonify({
        "message":f"Company {new_company.name} added!",
        "company_id":new_company.id
    }),201
