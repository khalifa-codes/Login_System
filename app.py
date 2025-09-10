from types import MethodDescriptorType
from flask import Flask, flash, redirect, render_template_string,url_for,g, request,render_template
import sqlite3,datetime,os

app = Flask(__name__)
database = "database/Credit.db"
app.secret_key = "supersecret123"
def get_db():
    db = getattr(g,"_database",None)
    if db is None:
        os.makedirs("database", exist_ok=True)
        db = g._database = sqlite3.connect(database)
        db.execute("CREATE TABLE IF NOT EXISTS CREDITS(NAME TEXT NOT NULL , ID INT NOT NULL UNIQUE, PASS TEXT NOT NULL, EMAIL TEXT NOT NULL)")
        db.commit()
    return db
@app.route("/",methods=["GET"])
def home():
    return render_template("home.html")

@app.route("/register",methods=["GET","POST"])
def register():
    db = get_db()
    cursor = db.cursor()
    if request.method == "POST":
        name = request.form['name']
        use_id = request.form["id"]
        pwd = request.form["pwd"]
        mail = request.form['email']
        action = request.form.get("register")
        if action == "register":
            print("works")
            try:
                cursor.execute("INSERT INTO CREDITS(NAME,ID,PASS,EMAIL) VALUES(?,?,?,?)",(name,use_id,pwd,mail))
                db.commit()
                return render_template("login.html")
            except sqlite3.IntegrityError:
                flash(f"  ID already exist","info")
    return render_template("register.html")

@app.route("/login",methods = ["GET","POST"])
def login():
    db = get_db()
    cursor = db.cursor()
    if request.method == "POST":
        id = request.form['id']
        pwd = request.form['pwd']
        action = request.form.get('login')
        if action == "login":
            cursor.execute(f"SELECT PASS FROM CREDITS WHERE ID ={id}")
            row = cursor.fetchone()
            if row and row[0] == pwd:
                credits = cursor.execute(f"SELECT NAME,ID,EMAIL FROM CREDITS WHERE ID = {id}")
                credits = cursor.fetchone()
                db.commit()
                return redirect(url_for("dashboard",name=credits[0]))
            flash(f"Wrong Creditentials","danger")
    return render_template("login.html")

@app.route("/dashboard",methods=['GET'])
def dashboard():
    name = request.args.get('name')
    return render_template("dashboard.html", name=name)

if __name__ == "__main__":
    app.run(debug=True)
