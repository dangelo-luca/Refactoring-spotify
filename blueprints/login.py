from flask import Blueprint, request, redirect, url_for, flash, render_template, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User

# Blueprint per il login
login_bp = Blueprint('login', __name__)

# Configurazione di Flask-Login
login_manager = LoginManager()
login_manager.login_view = "login.login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@login_bp.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if User.query.filter_by(username=username).first():
            flash("Questo username è già in uso.", "error")
            return render_template('register.html', error="Questo username è già in uso.")
        
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash("Registrazione completata con successo.", "success")
        return redirect(url_for('home.home'))
    
    return render_template('register.html', error=None)

@login_bp.route('/login-flask', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            session['user_id'] = user.id
            flash("Login effettuato con successo.", "success")
            return redirect(url_for('home.home'))
        
        flash("Credenziali non valide.", "error")
        return render_template('login.html', error="Credenziali non valide.")
    
    return render_template('login.html', error=None)

@login_bp.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('user_id', None)
    flash("Logout effettuato con successo.", "success")
    return redirect(url_for('login.login'))
