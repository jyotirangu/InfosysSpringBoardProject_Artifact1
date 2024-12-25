from flask import Blueprint, jsonify, request
from .model import db
from .model import Course, User
from .email import send_email

# Create a Blueprint for course-related routes
artifact_2BP = Blueprint('course', __name__)

# Route to get all courses
@artifact_2BP.route('/courses', methods=['GET'])
def get_courses():
    try:
        # Query all courses from the database
        # courses = Course.query.all()
         # Fetch all courses ordered by start_date in descending order
        courses = Course.query.order_by(Course.start_date.desc()).all()

        # Format courses into a list of dictionaries
        course_list = [
            {
                "id": course.id,
                "course_id": course.course_id,
                "title": course.title,
                "description": course.description,
                "instructor": course.instructor,
                "start_date": course.start_date,
                "end_date": course.end_date,
                "duration": course.duration,
                "created_by": {
                    "id": course.created_by,
                    "name": User.query.get(course.created_by).name,
                    "email": User.query.get(course.created_by).email
                }
            }
            for course in courses
        ]

        return jsonify({"courses": course_list}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@artifact_2BP.route('/addCourse', methods=['POST'])
def add_course():
    try:
        # Parse incoming JSON data
        data = request.get_json()

        # Extract and validate fields
        course_id = data.get('course_id')
        title = data.get('title')
        description = data.get('description')
        instructor = data.get('instructor')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        duration = data.get('duration')
        created_by = data.get('created_by')

        if not all([course_id, title, description, instructor, start_date, end_date, duration, created_by]):
            return jsonify({"error": "All fields are required!"}), 400

        # Check if the user exists
        user = User.query.get(created_by)
        if not user:
            return jsonify({"error": f"User with ID {created_by} not found!"}), 404

        # Create a new course
        new_course = Course(
            course_id=course_id,
            title=title,
            description=description,
            instructor=instructor,
            start_date=start_date,
            end_date=end_date,
            duration=duration,
            created_by=created_by
        )
        db.session.add(new_course)
        db.session.commit()

        # Fetch all user emails
        users = User.query.all()
        recipient_emails = [user.email for user in users]

        # Send email to each recipient one by one
        for email in recipient_emails:
            print(email)
            if email == "jyotirangu657@gmail.com" :
                continue
            send_email(
                sender_email="jyotirangu657@gmail.com",
                sender_password="avwt sldu agas ndpf",  # Ensure this is secure and not hardcoded
                recipient_email=email,  # Sending to one recipient at a time
                subject="New Course Added",
                body=f"A new course titled '{title}' has been added. Check it out! \nStart date : '{start_date}' \nDuration : '{duration} days'",
                attachment_path=None
            )

        return jsonify({"message": "Course added successfully! and Email has been sent Successfully", "course": {
            "id": new_course.id,
            "course_id": new_course.course_id,
            "title": new_course.title,
            "description": new_course.description,
            "instructor": new_course.instructor,
            "start_date": new_course.start_date,
            "end_date": new_course.end_date,
            "duration": new_course.duration,
            "created_by": {
                "id": user.id,
                "name": user.name,
                "email": user.email
            }
        }}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@artifact_2BP.route('/instructor', methods=['GET'])
def get_instructors():
    try:
        # Query all users with the role of "instructor"
        instructors = User.query.filter_by(role='Instructor').all()

        # Format the data as JSON
        instructor_list = [
            {
                'id': instructor.id,
                'name': instructor.name,
                'email': instructor.email,
                'role': instructor.role,
                'isVerified': instructor.isVerified
            } for instructor in instructors
        ]

        return jsonify({
            'status': 'success',
            'instructors': instructor_list
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500
        
 
# Create a new route in your backend for handling PUT requests to update a course.       
@artifact_2BP.route("/editCourse/<int:course_id>", methods=["POST", "PUT"])
def edit_course(course_id):
    try:
        data = request.get_json()
        course = Course.query.get(course_id)

        if not course:
            return jsonify({"error": "Course not found!"}), 404

        # Update course fields
        course.title = data.get("title", course.title)
        course.description = data.get("description", course.description)
        course.start_date = data.get("start_date", course.start_date)
        course.end_date = data.get("end_date", course.end_date)
        course.duration = data.get("duration", course.duration)

        db.session.commit()
        return jsonify({"message": "Course updated successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Add a Route for Deleting a Course: Create a route for handling DELETE requests.
@artifact_2BP.route("/deleteCourse/<int:course_id>", methods=["POST", "DELETE"])
def delete_course(course_id):
    try:
        course = Course.query.get(course_id)

        if not course:
            return jsonify({"error": "Course not found!"}), 404

        db.session.delete(course)
        db.session.commit()
        return jsonify({"message": "Course deleted successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
