from flask import Flask, jsonify, request, Blueprint,g
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from .model import db
# JWTManager is the main interface provided by flask_jwt_extended to integrate JWT functionality into your Flask application
# create_access_token is used to generate a JWT for a user after successful authentication (like after login).
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
)


app = Flask(__name__)

# It creates an instance of JWTManager and binds it to your Flask application instance (app). This makes JWT-related features available throughout your Flask app.
jwt = JWTManager(app)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:1234@localhost:5432/Infosys"
# It’s not specifically related to JWTs but is essential for overall app security.
app.config['SECRET_KEY'] = 'your_secret_key'
# The JWT_SECRET_KEY is used to generate a secure signature for JWTs, allowing the server to verify the authenticity of tokens.
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'

# db = SQLAlchemy(app)
db.init_app(app)
migrate = Migrate(app, db)

# Create the database tables if they don't exist
with app.app_context():
    from .artifact import artifact_1BP
    from .artifact2 import artifact_2BP
    db.create_all()
    
# Register the Blueprint for the artifact routes   
app.register_blueprint(artifact_1BP)
app.register_blueprint(artifact_2BP)

@app.route("/")
def hello_world():
    return "<p>Hello World</p>"



if __name__ == "__main__":
    app.run(debug=True)
    
    
    # https://github.com/jyotirangu/InfosysSpringBoardProject_Artifact1.git