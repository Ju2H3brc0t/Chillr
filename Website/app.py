from flask import Flask, render_template, request, redirect, url_for, session
import secrets
import json

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

def load_users():
    with open("users.json", "r") as file:
        return json.load(file)

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        users = load_users()

        if username in users and users[username] == password:
            session["user"] = username
            return redirect(url_for("dashboard"))
        else:
            return render_template("index.html", error="Authentication failed")

    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    return f"Bienvenue {session['user']} ! <a href='/logout'>Se déconnecter</a>"

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)


