from flask import Flask, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html", title = "Home")

# ----- Small API -----
@app.get("/api/health")
def health_check():
    return jsonify(status = "OK")  

if __name__ == '__main__':
    app.run(debug=True)


