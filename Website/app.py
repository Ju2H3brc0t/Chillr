from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify
import json

app = Flask(__name__)

def load_users():
    with open('users.json', 'r') as f:
        return json.load(f)

@app.route('/')
def home():
    return "Bienvenue sur la page d'accueil !"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        users = load_users()
        
        if username in users and users[username] == password:
            resp = make_response(redirect(url_for('home')))
            resp.set_cookie('username', username)
            return resp
        else:
            return render_template('index.html', error="Nom d'utilisateur ou mot de passe incorrect")
    return render_template('index.html')

@app.route('/logout')
def logout():
    resp = make_response(redirect('/login'))
    resp.delete_cookie('username')
    return resp

if __name__ == '__main__':
    app.run(debug=True)



