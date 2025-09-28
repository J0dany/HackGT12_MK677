import os
from flask import Flask, request, jsonify, render_template

# Import parser + models
from parser import parse_degreeworks_remaining
from models import Course, Term, Roadmap

app = Flask(__name__)
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


# ----- Small API -----
@app.get("/api/health")
def health_check():
    return jsonify(status = "OK")  

if __name__ == '__main__':
    app.run(debug=True)


