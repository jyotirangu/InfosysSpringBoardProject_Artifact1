from .model import User, db
from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
# from . import socketio  # Import the socketio instance from the __init__.py file
# from . import activeSession
# Now you can use socketio in this file for event handling or emitting messages


artifact_1BP = Blueprint('artifact_1', __name__)

# Route to sign up
@artifact_1BP.route("/register", methods=["POST"])
def signup():
    try:
        # Parse incoming JSON data
        data = request.get_json()       # This means I'm taking data in JSON format only, for other format it will deny or show error
        
        # Extract and validate fields
        name = data.get("name")
        email = data.get("email")
        password = data.get("password")
        role = data.get("role")  
        answer = data.get("answer")
        

        if not name or not email or not password:
            return jsonify({"error": "Name, Email, and Password are required!"}), 400

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Create a new user
        new_user = User(name=name, email=email, password=hashed_password, role=role, isVerified="False", answer=answer)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "User created successfully!", "user": {
            "name": name,
            "email": email,
            "role": role
        }}), 201
    except Exception as e:
        return jsonify({"error":str(e)}),500




    
# Route to Login

@artifact_1BP.route("/login", methods=["POST"])
def login():
    
        # Parse incoming JSON data
        data = request.get_json()
    
        # Extract and validate fields
        email = data.get("email")
        password = data.get("password")
        role = data.get("role")
        
        if not email or not password or not role:
            return jsonify({"error": "Email, Password and role are required!"}), 400
        
        
        # Query user from the database
        user = User.query.filter_by(email=email).first()
        # print(hashed_password)
        # print(user.password)

        if not user:
            return jsonify({"error": "User not found!"}), 404

        # Verify role
        if user.role != role:
            return jsonify({"error": f"Role mismatch: Expected {user.role}, got {role}"}), 403

        # Check password
        # Check the hashed password
        if not check_password_hash(user.password, password):
            return jsonify({"error": "Invalid password!"}), 401
        
        # Verify the Password
        if( user.isVerified == "False"):
            return jsonify({"error": "Not Verified"}), 401

    #    
        # Login successful
        return jsonify({"message": "Login successful!", "user": {"id": user.id, "name": user.name, "email": user.email, "role": user.role}}), 200
    


# Route to forget password

@artifact_1BP.route("/forgetpassword", methods=["POST"])
def forgetpassword():
    # Parse incoming JSON data
    data = request.get_json()
        
    # Extract and validate fields
    email = data.get("email")
    answer = data.get("answer")
    newPassword = data.get("newPassword")
    
    hashed_password = generate_password_hash(newPassword)
    
    if not email or not answer:
        return jsonify({"error": "Email and security answer are required!"}), 400
    
    # Query user from the database
    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"error": "User not found!"}), 404

    # Verify the answer
    if user.answer != answer:
        return jsonify({"error": "Security answer is incorrect!"}), 403
    
    # Update the password in the database
    user.password = hashed_password
    db.session.commit()

    return jsonify({"message": "Password updated successfully!"}), 200
