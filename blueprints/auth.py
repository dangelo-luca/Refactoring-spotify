from flask import Blueprint, request, redirect, url_for, session
from Services.spotify_oauth import sp_oauth

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login')
def login():    
    auth_url = sp_oauth.get_authorize_url() #login di spotify
    return redirect(auth_url)

@auth_bp.route('/callback')
def callback():
    code = request.args.get('code') #recupero codice di autorizzazione
    token_info = sp_oauth.get_access_token(code) #uso il code per un codice di accesso
    session['token_info'] = token_info #salvo il token nella mia sessione x riutilizzarlo
    return redirect(url_for('home.home'))

@auth_bp.route('/disconetti')
def disconetti():
    session.pop('token_info', None)  # Rimuove solo il token di accesso dalla sessione
    return redirect(url_for('home.home'))  # Torna alla home senza forzare il login
