from flask import Blueprint, request, redirect, url_for, session, flash, render_template
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from Services.spotify_oauth import sp_oauth

# Blueprint per l'autenticazione
login_bp = Blueprint('login', __name__)

# Configurazione di Flask-Login
login_manager = LoginManager()
login_manager.login_view = "login.login_page"

# Modello utente
class User(UserMixin):
    def __init__(self, user_id, token_info):
        self.id = user_id
        self.token_info = token_info

@login_manager.user_loader
def load_user(user_id):
    token_info = session.get('token_info')
    if token_info:
        return User(user_id, token_info)
    return None

@login_bp.route('/login-flask')
def login_page():    
    return render_template("login.html")  # Mostra la pagina di login

@login_bp.route('/spotify-login')
def spotify_login():
    auth_url = sp_oauth.get_authorize_url()  # URL di autorizzazione Spotify
    return redirect(auth_url)


@login_bp.route('/logout-flask')
@login_required
def logout():
    session.clear()  # Pulizia sessione
    logout_user()  # Logout con Flask-Login
    flash("Logout effettuato con successo.", "success")
    return redirect(url_for('login.login_page'))