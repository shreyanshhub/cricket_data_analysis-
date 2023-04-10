from flask import Flask,request,render_template,redirect,url_for,flash,session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "data"

db = SQLAlchemy(app)

class User(db.Model):

    id = db.Column("id",db.Integer,primary_key = True)
    username = db.Column("username",db.String(100))
    password = db.Column("password",db.String(100))

    def __init__(self,username,password):

        self.username = username
        self.password = password

@app.route("/<username>",methods=["GET","POST"])
def home(username):
    if "username" in session:
        return render_template("home.html",username=username)
    return "<h1>Welcome </h1>"

@app.route("/register_user",methods=["GET","POST"])
def register_user():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        number = "1234567890"

        if len(password) <= 8:
            flash(" Min Length of password should be 8")
            return render_template("register_user.html")

        count = 1
        for x in number:
            if count != 10:
                if x not in password:
                    count += 1
                    continue
                else:
                    break
            else:
                if x not in password:
                    flash("There should be min 1 numeric character in password")
                    return render_template("register_user.html")


        special = "!@#$%^&*()"

        count = 1
        for x in number:
            if count != 10:
                if x not in password:
                    count += 1
                    continue
                else:
                    break
            else:
                if x not in password:
                    flash("There should be min 1 special character in password")
                    return render_template("register_user.html")



        usr = User.query.filter_by(username=username).first()

        if usr:
            flash("Username already exists","info")
            return render_template("register_user.html")

        else:
            '''
            session["username"]  = username
            session["password"] = password '''


            user = User(username = username,password = password)


            db.session.add(user)
            db.session.commit()

            flash("User registered successfully","info")
            return redirect(url_for("login_user"))



    return render_template("register_user.html")

@app.route("/login_user",methods=["GET","POST"])
def login_user():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username,password=password).first()

        if user:
            return redirect(url_for("home",username=username))
        else:
            flash("Username or password is incorrect","info")
            return render_template("login_user.html")

    return render_template("login_user.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug = True , port=8002)
