import os
from flask import Flask, request, jsonify, render_template

# Import parser + models
from degreeworks.routes.parser import parse_degreeworks_remaining
from Models.models import Course, Term, Roadmap

app = Flask(__name__, template_folder='frontend')
app.config["UPLOAD_FOLDER"] = "uploads"

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
    """Create a sample roadmap from remaining courses"""
    return {
        "terms": [
            {
                "name": "Fall 2025",
                "credits": 15,
                "courses": [
                    {"code": "CS 301", "name": "Database Systems", "credits": 3},
                    {"code": "CS 302", "name": "Software Engineering", "credits": 3},
                    {"code": "MATH 301", "name": "Statistics", "credits": 3},
                    {"code": "ENG 201", "name": "Technical Writing", "credits": 3},
                    {"code": "PHYS 101", "name": "Physics I", "credits": 3}
                ]
            },
            {
                "name": "Spring 2026", 
                "credits": 15,
                "courses": [
                    {"code": "CS 401", "name": "Operating Systems", "credits": 3},
                    {"code": "CS 402", "name": "Computer Networks", "credits": 3},
                    {"code": "CS 403", "name": "Machine Learning", "credits": 3},
                    {"code": "PHIL 101", "name": "Ethics", "credits": 3},
                    {"code": "ART 101", "name": "Digital Art", "credits": 3}
                ]
            }
        ],
        "summary": {
            "terms_remaining": 2,
            "credits_remaining": 30,
            "graduation_date": "Spring 2026"
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


