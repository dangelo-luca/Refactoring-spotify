from flask import Blueprint, request, redirect, url_for, flash, render_template
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# Blueprint per il login
login_bp = Blueprint('login', __name__)

# Configurazione di Flask-Login
login_manager = LoginManager()
login_manager.login_view = "login"

# Inizializzazione del database
db = SQLAlchemy()

# Modello utente
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@login_bp.route('/login-flask', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            flash("Login effettuato con successo!", "success")
            return redirect(url_for('home.home'))
        else:
            flash("Credenziali non valide.", "danger")
    
    return render_template("login.html")

@login_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if User.query.filter_by(username=username).first():
            flash("Questo username è già in uso.", "danger")
            return redirect(url_for('login.register'))
        
        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash("Registrazione completata! Ora puoi effettuare il login.", "success")
        return redirect(url_for('login.login_page'))
    
    return render_template("register.html")

@login_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logout effettuato con successo.", "success")
    return redirect(url_for('login.login_page'))