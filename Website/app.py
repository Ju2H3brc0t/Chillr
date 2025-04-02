from flask import Flask, render_template, request, redirect, url_for, session, jsonify, make_response
import json
import yaml
import os

app = Flask(__name__)
app.secret_key = 'secret_key'

def load_config(config_file="website_config.yaml"):
    dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(dir, config_file)

    if not os.path.exists(path):
        raise FileNotFoundError("Configuration file not found")

    with open(path, "r") as file:
        return yaml.safe_load(file)
    
config = load_config()

file_path = config['path']['users']

def load_users():
    with open(file_path, 'r', encoding="utf-8") as f:
        return json.load(f)

print(f"Reading file: {file_path}")
if not os.path.exists(file_path):
    print("File not found")
else:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        print("File content:")
        print(content)

@app.route("/")
def home():
    session = request.cookies.get("session")
    if session:
        return redirect("/dashboard")
    return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        users = load_users()

        if username in users and users[username] == password:
            resp = make_response(redirect("/dashboard"))
            resp.set_cookie("session", username)
            print(f"User {username} logged in successfully.")
            return resp

        return redirect("/login")
        print(f"Failed login attempt for user {username}.")

    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    session = request.cookies.get("session")
    if not session:
        return redirect("/login")
    return render_template("dashboard.html", username=session)

@app.route("/logout", methods=["POST"])
def logout():
    resp = make_response(redirect("/login"))
    resp.set_cookie("session", "", expires=0)
    return resp

if __name__ == "__main__":
    app.run(debug=True)