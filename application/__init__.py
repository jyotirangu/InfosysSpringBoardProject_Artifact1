from flask import Flask, jsonify, request, Blueprint,g
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from .model import db

from flask_socketio import SocketIO
# from flask_socketio import SocketIO



app = Flask(__name__)
# socketio = SocketIO(app)
# g.activeSession = "notDefined"
# Enable CORS for all routes
# CORS(app)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})


socketio = SocketIO(app, cors_allowed_origins="*")

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:1234@localhost:5432/Infosys"
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
    
    
# echo "# InfosysSpringBoardProject_Artifact1" >> README.md
# git init
# git add .
# git commit -m "first commit"
# git branch -M main
# git remote add origin https://github.com/jyotirangu/InfosysSpringBoardProject_Artifact1.git
# git push -u origin main

# git remote add origin https://github.com/jyotirangu/InfosysSpringBoardProject_Artifact1.git
# // git branch -M main
# // git push -u origin ma