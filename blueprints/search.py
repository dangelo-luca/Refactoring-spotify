from flask import Blueprint, render_template, redirect, url_for, session
from Services.spotify_oauth import get_spotify_object


search_bp = Blueprint('search', __name__)
