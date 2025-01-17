from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["MYSQL_HOST"] = "138.41.20.102"
app.config["MYSQL_PORT"] = 53306
app.config["MYSQL_DB"] = "w3schools"
app.config["MYSQL_USER"] = "ospite"
app.config["MYSQL_PASSWORD"] = "ospite"
mysql = MySQL(app)

app.secret_key = "segretissimo"

@app.route("/")
def home():
    return render_template("home.html", titolo="Home")

@app.route("/register/", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html", titolo="Registrati")
    
    nome = request.form.get("nome", "Stringa Vuota")
    cognome = request.form.get("cognome", "Stringa Vuota")
    username = request.form.get("username", "Stringa Vuota")
    password = request.form.get("password", "Stringa Vuota")
    confermaPassword = request.form.get("confermaPassword", "Stringa Vuota")
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    tmp = cursor.fetchall()
    cursor.close()
    if len(tmp)>0:
        return render_template("errore.html", titolo = "Errore", errore = "username già esistente")
    if(nome == "Stringa Vuota" or cognome == "Stringa Vuota" or username == "Stringa Vuota" or password == "Stringa Vuota" or password != confermaPassword):
        return render_template("errore.html", titolo = "Errore")
    else:
        cursor = mysql.connection.cursor()
        query = "INSERT INTO users VALUES(%s, %s, %s, %s)"
        cursor.execute(query, (username, generate_password_hash(password), nome, cognome))
        mysql.connection.commit()
        cursor.close()
        flash('Ti sei registrato')
        flash('Secondo messaggio')
        return redirect(url_for('home'))

@app.route("/login/", methods = ["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", titolo="Login")
    
    username = request.form.get("username")
    password = request.form.get("Password")
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM users WHERE username = %s"
    cursor.execute(query, (username, ))
    tmp = cursor.fetchall()
    cursor.close()

    if len(tmp)==0:
        flash("Username non esistente")
        return redirect(url_for('login'))
    
    if check_password_hash(generate_password_hash(password), password):
        flash("Benvenuto" + str(username))
        return redirect(url_for('session'))
    
    flash("Password errata")
    return redirect(url_for('login'))

@app.route("/session")
def session():
    return render_template("session.html", titolo="Session")

app.run(debug=True)
