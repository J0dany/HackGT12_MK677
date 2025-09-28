from flask import Flask, jsonify
from routes.upload import upload_bp

app = Flask(__name__)

# register blueprint (like FastAPI include_router)
app.register_blueprint(upload_bp, url_prefix="/api")

@app.route("/")
def root():
    return jsonify(message="DegreeWorks PDF Remaining Courses Parser API")

if __name__ == "__main__":
    app.run(debug=True)
