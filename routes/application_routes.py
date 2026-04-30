import os
from google import genai
from flask_migrate import Migrate
from flask import Blueprint, jsonify, request
from extensions import db
from models.job_application import JobApplication
from flask_jwt_extended import jwt_required, get_jwt_identity


# Create the Blueprint
application_bp = Blueprint('applications', __name__)

# WAITER 1: GET (Read all applications)
@application_bp.route('/applications', methods=['GET'])
@jwt_required()
def get_applications():
    current_user_id=get_jwt_identity()
    user_apps = JobApplication.query.filter_by(user_id=current_user_id).all()
    status_filter=request.args.get('status')
    page=request.args.get('page',1,type=int)
    per_page=request.args.get('per_page',10,type=int)
    query=JobApplication.query.filter_by(user_id=current_user_id)
    if status_filter:
        query=query.filter_by(status=status_filter)
    paginated_apps=query.paginate(page=page,per_page=per_page,error_out=False)
    app_list = []
    
    for app in paginated_apps.items:
        app_list.append({
            "id": app.id,
            "role": app.role,
            "status": app.status,
            "company_nane": app.company.name if app.company else "unknown"
        })
        
    return jsonify({
        "total_applications":paginated_apps.total,
        "current_page":paginated_apps.page,
        "total_pages":paginated_apps.pages,
        "applications":app_list
    }), 200

# WAITER 2: POST (Add a new application)
@application_bp.route('/applications', methods=['POST'])
@jwt_required()
def add_application():

    current_user_id=get_jwt_identity()
    data=request.get_json()
    
    if not data.get('role') or not data.get('company_id'):
        return jsonify({"error":"Role and company id are strictly required."}),400
    valid_status=['Applied','Interviewing','Rejected','Offer']
    incoming_status=data.get('status','Applied')

    if incoming_status not in valid_status:
        return jsonify({"error": f"Invalid status. Must be one of {valid_status}"}),400
    incoming_round=data.get('current_round','Initial Application')
    new_app = JobApplication(
        role=data.get('role'),
        status=incoming_status,
        user_id=current_user_id,
        company_id=data.get('company_id'),
        current_round=incoming_round
    )
    
    db.session.add(new_app)
    db.session.commit()
    
    return jsonify({"message": "Application added successfully!"}), 201

@application_bp.route('/applications/<int:app_id>', methods=['DELETE'])
@jwt_required()
def delete_application(app_id):
    current_user_id=get_jwt_identity()
    
    app_to_delete = JobApplication.query.get(app_id)
    
    
    if not app_to_delete:
        return jsonify({"error": "Application not found"}), 404
    if app_to_delete.user_id!=current_user_id:
        return jsonify({"error":"you do not own this application"}),403
        
    
    db.session.delete(app_to_delete)
    db.session.commit()
    
    return jsonify({"message": f"Application {app_id} deleted successfully!"}), 200
# WAITER 4: PUT (Update an application)
@application_bp.route('/applications/<int:app_id>', methods=['PUT'])
@jwt_required()
def update_application(app_id):
    from flask import request
    current_user_id=get_jwt_identity()
    
    app_to_update = JobApplication.query.get(app_id)
    
    
    if not app_to_update:
        return jsonify({"error": "Application not found"}), 404
    if app_to_update.user_id!=current_user_id:
        return jsonify({"error: you do not own this application"}),403
        
    
    data = request.get_json()
    allowed_fields=['role','status','company_id']
    valid_status=['Applied','Interviewing','Rejected','Offer']
    for key,value in data.items():
        if key in allowed_fields:
            if key=='status' and value not in valid_status:
                return jsonify({"error":f"Invalid Status. Must be one of {valid_status}"}),400
            setattr(app_to_update,key,value)
    
    db.session.commit()
    
    return jsonify({"message": f"Application {app_id} updated successfully!"}), 200
@application_bp.route('/<int:app_id>/interview_prep',methods=['POST'])
@jwt_required()
def generate_interview_prep(app_id):
    current_user_id=get_jwt_identity()
    job_app=JobApplication.query.filter_by(id=app_id,user_id=current_user_id).first()
    if not job_app:
        return jsonify({"error":"Application not found or unauthorized."}),404
    data=request.get_json(silent=True) or {}
    action=data.get('action','initial_questions')
    previous_data=data.get('previous_data','')

    base_prompt=f"""
    I am a candidate applying for a {job_app.role} role. 
    I am preparing for the "{job_app.current_round}" interview round.
    """
    if job_app.notes:
        base_prompt+=f"Here is my personal note: '{job_app.notes}'. Tailor your response heavily to this context."
    if action=='answers':
        instruction=f"Here are the questions I was asked: \n{previous_data}\n Provide highly technical, professional answers to these specific questions."
    elif action=='more_questions':
        instruction="Provide exactly 5 highly specific interview questions I should prepare for. Format clearly."
    else: 
        # THE SAFETY NET: This catches 'initial_questions' and any random typos
        instruction = "Provide exactly 5 highly specific interview questions I should prepare for. Format clearly."
    full_prompt=base_prompt + instruction
    try:
        client=genai.Client(api_key=os.getenv('GEMINI_API_KEY'))
        response=client.models.generate_content(
            model='gemini-2.5-flash',
            contents=full_prompt
        )
        return jsonify({
            "action_executed":action,
            "job_role":job_app.role,
            "note_used":job_app.notes if job_app.notes else "None",
            "ai_response":response.text
        }),200
    except Exception as e:
        return jsonify({"error":f"AI integration failed: {str(e)}"}),500
# WAITER 5: PUT (Update an existing job application)
@application_bp.route('/<int:app_id>', methods=['PUT'])
@jwt_required()
def update_application(app_id):
    current_user_id = get_jwt_identity()
    
    # 1. THE SECURITY CHECK: Find the exact job
    job_app = JobApplication.query.filter_by(id=app_id, user_id=current_user_id).first()
    
    if not job_app:
        return jsonify({"error": "Application not found or unauthorized."}), 404

    # 2. GET THE NEW DATA
    data = request.get_json(silent=True) or {}
    
    # 3. UPDATE THE COLUMNS (Only if the user actually sent new data)
    if 'status' in data:
        job_app.status = data['status']
    
    if 'current_round' in data:
        job_app.current_round = data['current_round']
        
    # IMPORTANT: Change 'note' to 'notes' here if your models.py uses the plural!
    if 'notes' in data:  
        job_app.notes = data['notes']

    # 4. SAVE TO THE DATABASE
    try:
        db.session.commit() # This officially locks the changes into the SQLite file
        return jsonify({
            "message": "Application updated successfully!",
            "status": job_app.status,
            "current_round": job_app.current_round,
            "notes": job_app.notes 
        }), 200
        
    except Exception as e:
        db.session.rollback() # If the database crashes, cancel the save to prevent corruption
        return jsonify({"error": f"Database update failed: {str(e)}"}), 500