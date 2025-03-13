from flask import Flask
from flask_login import LoginManager
from blueprints.login import login_bp, login_manager
from blueprints.home import home_bp
from blueprints.artisti import artisti_bp
from blueprints.auth import auth_bp

app = Flask(__name__)
app.secret_key = 'chiavesessione'

# Inizializza Flask-Login
login_manager.init_app(app)

# Registra i blueprint
app.register_blueprint(auth_bp)
app.register_blueprint(login_bp)
app.register_blueprint(home_bp)
app.register_blueprint(artisti_bp)


if __name__ == "__main__":
    app.run(debug=True)