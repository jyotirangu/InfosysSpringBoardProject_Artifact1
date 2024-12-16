from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:1234@localhost:5432/Infosys"
db = SQLAlchemy(app)


class User(db.Model):
    _tablename_ = 'Infosys_user'  # Table name

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)  # Password should be hashed
    role = db.Column(db.String(50), nullable=False, default='basic')
    isVerified = db.Column(db.String(20), nullable=False)
    answer = db.Column(db.String(50), nullable=False)
    # created_at = db.Column(db.String(20),nullable=False)

migrate = Migrate(app, db)

@app.route("/")
def hello_world():
    return "<p>Hello World</p>"

# Route to sign up
@app.route("/register", methods=["POST"])
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
        # hashed_password = generate_password_hash(password)

        # Create a new user
        new_user = User(name=name, email=email, password=password, role=role, isVerified="False", answer=answer)
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

@app.route("/login", methods=["POST"])
def login():
    
        # Parse incoming JSON data
        data = request.get_json()
        
        # Extract and validate fields
        email = data.get("email")
        password = data.get("password")
        role = data.get("role")
        
        if not email or not password or not role:
            return jsonify({"error": "Email, Password and role are required!"}), 400

        # Hash the password
        # hashed_password = generate_password_hash(password)
        
        # Query user from the database
        user = User.query.filter_by(email=email).first()

        if not user:
            return jsonify({"error": "User not found!"}), 404

        # Verify role
        if user.role != role:
            return jsonify({"error": f"Role mismatch: Expected {user.role}, got {role}"}), 403

        # Check password
        if (user.password != password):
            return jsonify({"error": "Invalid password!"}), 401
        
        # Verify the Password
        if( user.isVerified == "False"):
            return jsonify({"error": "Not Verified"}), 401

        # Login successful
        return jsonify({"message": "Login successful!", "user": {"id": user.id, "name": user.name, "email": user.email, "role": user.role}}), 200
    


# Route to forget password

@app.route("/forgetpassword", methods=["POST"])
def forgetpassword():
    # Parse incoming JSON data
    data = request.get_json()
        
    # Extract and validate fields
    email = data.get("email")
    answer = data.get("answer")
    newPassword = data.get("newPassword")
    
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
    user.password = newPassword
    db.session.commit()

    return jsonify({"message": "Password updated successfully!"}), 200
    


if __name__ == "__main__":
    app.run(debug=True)
    
    
# echo "# InfosysSpringBoardProject_Artifact1" >> README.md
# git init
# git add README.md
# git commit -m "first commit"
# git branch -M main
# git remote add origin https://github.com/jyotirangu/InfosysSpringBoardProject_Artifact1.git
# git push -u origin main