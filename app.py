from flask import Flask, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html", title = "Home")

@app.route('/api/upload-transcript')
def upload_transcript():
    return render_template("upload_transcript.html", title = "Upload Transcript")

@app.route('/api/manual-entry')
def manual_entry():
    return render_template("manual_entry.html", title = "Manual Entry")


# ----- Small API -----
@app.get("/api/health")
def health_check():
    return jsonify(status = "OK")  

if __name__ == '__main__':
    app.run(debug=True)


