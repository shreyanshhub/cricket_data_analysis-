from flask import Flask,request,render_template,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "data"

db = SQLAlchemy(app)

@app.route("/")
def home():
    return "<h1>Welcome </h1>"



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug = True , port=8002)
