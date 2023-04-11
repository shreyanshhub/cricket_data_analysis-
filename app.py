from flask import Flask,request,render_template,redirect,url_for,flash,session
from flask_sqlalchemy import SQLAlchemy
import csv

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

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    innings = db.Column(db.Integer)
    overs = db.Column(db.Float)
    ballnumber = db.Column(db.Integer)
    batter = db.Column(db.String(255))
    bowler = db.Column(db.String(255))
    non_striker = db.Column(db.String(255))
    extra_type = db.Column(db.String(255))
    batsman_run = db.Column(db.Integer)
    extras_run = db.Column(db.Integer)
    total_run = db.Column(db.Integer)
    non_boundary = db.Column(db.Boolean)
    is_wicket_delivery = db.Column(db.Boolean)
    player_out = db.Column(db.String(255))
    kind = db.Column(db.String(255))
    fielders_involved = db.Column(db.String(255))
    batting_team = db.Column(db.String(255))

def preprocess_data(data):
    # Separate categorical and numerical features
    cat_features = ["batter", "bowler", "non_striker", "extra_type", "player_out", "kind", "fielders_involved", "batting_team"]
    num_features = ["innings", "overs", "ballnumber", "batsman_run", "extras_run", "non_boundary", "is_wicket_delivery"]
    X_cat = data[cat_features]
    X_num = data[num_features]

    # Encode categorical features using one-hot encoding
    ct = ColumnTransformer(transformers=[("onehot", OneHotEncoder(), cat_features)], remainder="passthrough")
    X_cat_enc = ct.fit_transform(X_cat)

    # Scale numerical features
    scaler = StandardScaler()
    X_num_scaled = scaler.fit_transform(X_num)

    # Concatenate encoded categorical features and scaled numerical features
    X = pd.concat([pd.DataFrame(X_cat_enc.toarray()), pd.DataFrame(X_num_scaled, columns=num_features)], axis=1)

    # Extract target variable
    y = data["batsman_run"]

    print(X)
    print(y)
    return X, y


@app.route("/",methods=["GET","POST"])
def home():
    if request.method == "POST":

        batter_name = request.form["batter_name"]
        overs_less_than = request.form["overs"]
        batter_data = Data.query.filter(db.and_(Data.batter == batter_name, Data.overs <= float(overs_less_than))).all()

        return render_template("batter_data.html",batter_data=batter_data)

    return render_template("home.html")



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
