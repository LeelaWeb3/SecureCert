from flask import Flask, render_template, request, redirect, session, send_from_directory, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from utils import generate_hash, generate_pdf
from blockchain import add_certificate, get_certificate
import os

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = "secret123"

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default='user')

with app.app_context():
    db.create_all()
    if not User.query.filter_by(email="admin@mail.com").first():
        db.session.add(User(
            name="Admin",
            email="admin@mail.com",
            password=generate_password_hash("admin123"),
            role="admin"
        ))
        db.session.commit()

# ------------------ ROUTES ------------------

@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session["email"] = user.email
            session["role"] = user.role
            session["name"] = user.name
            return redirect(url_for("dashboard"))
        error = "Invalid login"
    return render_template("login.html", error=error)

@app.route("/signup", methods=["GET", "POST"])
def signup():
    error = None
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        if User.query.filter_by(email=email).first():
            error = "Email already registered"
        else:
            db.session.add(User(
                name=name,
                email=email,
                password=generate_password_hash(password)
            ))
            db.session.commit()
            return redirect(url_for("login"))
    return render_template("signup.html", error=error)

@app.route("/dashboard")
def dashboard():
    if "email" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html", name=session.get("name"), role=session.get("role"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# Admin: generate certificate
@app.route("/generate_form")
def generate_form():
    if session.get("role") != "admin":
        return "Access Denied"
    return render_template("generate.html")

@app.route("/generate", methods=["POST"])
def generate():
    if session.get("role") != "admin":
        return "Access Denied"

    cert_id = request.form.get("cert_id")
    email = request.form.get("email")
    name = request.form.get("name")
    course = request.form.get("course")

    cert_hash = generate_hash(email, course)
    try:
        add_certificate(cert_id, email, name, course, cert_hash)
    except Exception as e:
        return f"Blockchain error: {e}"

    filename = f"certificates/{cert_id}.pdf"
    generate_pdf(cert_id, name, email, course, cert_hash, filename)
    return f"Certificate generated! <a href='{url_for('serve_certificate', filename=cert_id+'.pdf')}'>Download PDF</a>"

@app.route("/certificates/<path:filename>")
def serve_certificate(filename):
    return send_from_directory("certificates", filename)

# Verify certificate
@app.route("/verify_form")
def verify_form():
    return render_template("verify.html")

@app.route("/verify", methods=["POST"])
def verify():
    cert_id = request.form.get("cert_id")
    email = request.form.get("email")
    cert = get_certificate(cert_id)
    if not cert:
        return "Certificate not found"
    if cert[4] == generate_hash(email, cert[3]):
        return "✅ Certificate is VALID"
    return "❌ Certificate is INVALID/TAMPERED"

if __name__ == "__main__":
    os.makedirs("certificates", exist_ok=True)
    app.run(debug=True, host="0.0.0.0", port=5001)