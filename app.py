from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config["MYSQL_HOST"] = "138.41.20.102"
app.config["MYSQL_PORT"] = 53306
app.config["MYSQL_DB"] = "w3schools"
app.config["MYSQL_USER"] = "ospite"
app.config["MYSQL_PASSWORD"] = "ospite"
mysql = MySQL(app)

@app.route("/")
def home():
    return render_template("home.html", titolo="Home")

@app.route("/register/", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html", titolo="Registrati")
    else:
        nome = request.form.get("nome")
        cognome = request.form.get("cognome")
        username = request.form.get("username")
        password = request.form.get("password")
        confermaPassword = request.form.get("confermaPassword")
        if(nome != None & cognome != None & username != None & password != None & password == confermaPassword):
            cursor = mysql.connection.cursor()
            query = "INSERT INTO users VALUES(%s, %s, %s, %s)"
            cursor.execute(query, (username, password, nome, cognome))
            mysql.connection.commit()
            cursor.close()
            return redirect(url_for('home'))
        else:
            

@app.route("/login")
def login():
    return render_template("login.html", titolo="Login")

@app.route("/session")
def session():
    return render_template("session.html", titolo="Session")

app.run(debug=True)
