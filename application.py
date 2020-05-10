import os
import requests

from flask import Flask, session, flash, redirect, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
#Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():

    return "Project 1: TODO"

@app.route("/register", methods=["GET", "POST"])
def register():

    #session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password_one = request.form.get("password1")
        recheck_pass = request.form.get("password2")

        if username == None:
            flash("Please, enter a username.")
            return redirect(url_for("/register"))

        if password_one != recheck_pass or password_one is None or recheck_pass is None:
            flash("Passwords do not match!")
            return redirect(url_for("/register"))

        hashed_password = generate_password_hash(request.form.get("password_one"), method='pbkdf2:sha256', salt_length=8)

        db.execute("INSERT INTO users (username, password) VALUES (:username, :password)", {"username": username, "password": hashed_password})

        db.commit()
    else:
        return render_template("register.html")
