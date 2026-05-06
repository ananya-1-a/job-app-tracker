from flask import Blueprint,request,jsonify
from extensions import db
from models.company import Company
from flask_jwt_extended import jwt_required 

company_bp=Blueprint('companies',__name__)
@company_bp.route('/companies', methods=['POST'])
@jwt_required()
def add_company():
    """
    Add a new company
    ---
    tags:
      - Companies
    security:
      - BearerAuth: []
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - name
          properties:
            name:
              type: string
              description: "The name of the company"
            location:
              type: string
              description: "e.g., Remote, Bangalore, On-site (Optional)"
            website:
              type: string
              description: "Company URL (Optional)"
    responses:
      201:
        description: Company added successfully
      400:
        description: Missing required fields
    """
    data = request.get_json()
    
    if not data.get('name'):
        return jsonify({"error": "Company name is required"}), 400
        
    new_company = Company(
        name=data.get('name'),
        location=data.get('location'),
        website=data.get('website')
    )
    db.session.add(new_company)
    db.session.commit()

    return jsonify({
        "message": f"Company {new_company.name} added!",
        "company_id": new_company.id
    }), 201