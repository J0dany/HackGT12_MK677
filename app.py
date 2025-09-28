import os
from flask import Flask, request, jsonify, render_template

# Import parser + models
from degreeworks.routes.parser import parse_degreeworks_remaining
from Models.models import Course, Term, Roadmap, Major
from services.database_service import GTDatabaseService
from semester_optimizer import build_roadmap

app = Flask(__name__, template_folder='frontend')
app.config["UPLOAD_FOLDER"] = "uploads"

# Initialize database service
db_service = GTDatabaseService()

@app.route('/')
def home():
    return render_template("index.html", title = "Home")

@app.route('/api/upload-transcript', methods=["GET", "POST"])
def upload_transcript():
    if request.method == "POST":
        if "file" not in request.files:
            return jsonify({"error": "No file part"}), 400

        file = request.files["file"]

        if file.filename == "":
            return jsonify({"error": "No selected file"}), 400

        os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(file_path)

        remaining_courses = parse_degreeworks_remaining(file_path)

        return jsonify({"remaining_courses": remaining_courses})

    # GET request just shows upload page
    return render_template("upload_transcript.html", title="Upload Transcript")

@app.route('/api/manual-entry')
def manual_entry():
    return render_template("manual_entry.html", title = "Manual Entry")

@app.route('/api/majors')
def get_majors():
    """Get all GT majors"""
    majors = db_service.get_all_majors()
    return jsonify([{
        'major_name': major.major_name,
        'college': major.college,
        'degree_type': major.degree_type,
        'description': major.description
    } for major in majors])

@app.route('/api/courses/<major_name>')
def get_courses_for_major(major_name):
    """Get courses for a specific major"""
    courses = db_service.get_courses_for_major(major_name)
    return jsonify({
        'core': [{
            'course_code': course.course_code,
            'course_name': course.course_name,
            'credits': course.credits,
            'average_gpa': course.average_gpa,
            'description': course.description
        } for course in courses['core']],
        'elective': [{
            'course_code': course.course_code,
            'course_name': course.course_name,
            'credits': course.credits,
            'average_gpa': course.average_gpa,
            'description': course.description
        } for course in courses['elective']],
        'prerequisite': [{
            'course_code': course.course_code,
            'course_name': course.course_name,
            'credits': course.credits,
            'average_gpa': course.average_gpa,
            'description': course.description
        } for course in courses['prerequisite']]
    })

@app.route('/api/courses/search/<query>')
def search_courses(query):
    """Search courses by name or code"""
    courses = db_service.search_courses(query)
    return jsonify([{
        'course_code': course.course_code,
        'course_name': course.course_name,
        'credits': course.credits,
        'average_gpa': course.average_gpa,
        'department': course.department,
        'description': course.description
    } for course in courses])

@app.route('/api/departments')
def get_departments():
    """Get all departments"""
    departments = db_service.get_departments()
    return jsonify(departments)

@app.route('/api/roadmap', methods=['POST'])
def generate_roadmap():
    """Generate roadmap from either PDF upload or manual entry"""
    if request.form.get('source') == 'pdf':
        # Handle PDF upload
        if "transcript" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400
        
        file = request.files["transcript"]
        if file.filename == "":
            return jsonify({"error": "No file selected"}), 400
        
        os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(file_path)
        
        remaining_courses = parse_degreeworks_remaining(file_path)
        
        # Generate sample roadmap for now
        roadmap = create_sample_roadmap(remaining_courses)
        return jsonify(roadmap)
    
    elif request.json and request.json.get('source') == 'manual':
        # Handle manual entry
        data = request.json
        major = data.get('major')
        completed_courses = data.get('completed_courses', [])
        
        # Generate sample roadmap for now
        roadmap = create_sample_roadmap_for_major(major, completed_courses)
        return jsonify(roadmap)
    
    return jsonify({"error": "Invalid request"}), 400

def create_sample_roadmap(remaining_courses):
    """Create a roadmap from remaining courses using real GT data"""
    # Convert remaining course codes to Course objects
    courses = []
    for course_code in remaining_courses:
        course = db_service.get_course_by_code(course_code)
        if course:
            courses.append(course)
    
    # If no courses found in database, create sample courses
    if not courses:
        courses = [
            Course("Database Systems", "CS 301", 3, average_gpa=3.2),
            Course("Software Engineering", "CS 302", 3, average_gpa=3.1),
            Course("Statistics", "MATH 301", 3, average_gpa=2.8),
            Course("Technical Writing", "ENG 201", 3, average_gpa=3.4),
            Course("Physics I", "PHYS 101", 3, average_gpa=2.9)
        ]
    
    # Create roadmap using database service
    roadmap = build_roadmap(
    courses=courses,
    num_terms=8,   # TODO: decide number of terms from frontend or logic
    preset_roadmap=None,
    max_hours=18,
    min_hours=12,
    allow_one_parttime=True
)
    
    # Convert to JSON format
    terms_data = []
    for term in roadmap.terms:
        term_data = {
            "name": term.term_name,
            "credits": sum(c.credits or 3 for c in term.courses),
            "courses": [{
                "code": c.course_code,
                "name": c.course_name,
                "credits": c.credits or 3,
                "average_gpa": c.average_gpa
            } for c in term.courses]
        }
        terms_data.append(term_data)
    
    return {
        "terms": terms_data,
        "summary": {
            "terms_remaining": len(roadmap.terms),
            "credits_remaining": roadmap.total_credits,
            "graduation_date": "TBD",
            "estimated_gpa": roadmap.estimated_gpa
        }
    }

def create_sample_roadmap_for_major(major, completed_courses):
    """Create a sample roadmap for manual entry"""
    return create_sample_roadmap([])

# ----- Small API -----
@app.get("/api/health")
def health_check():
    return jsonify(status = "OK")  

if __name__ == '__main__':
    app.run(debug=True)


