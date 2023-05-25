from flask import Blueprint, render_template
from flask_login import login_required, current_user
default_views = Blueprint('default_views',__name__)

@default_views.route('/home')
def home():
    return render_template('home.html')

@default_views.route('/contact')
def contact():
    return render_template('contact.html')

@default_views.route('/tokens')
def tokens():
    return render_template('tokens.html')

@default_views.route('/features')
def features():
    return render_template('features.html')

@default_views.route('/plans')
@login_required
def plans():
    return render_template('plans.html')

@default_views.route('/privacy_policy')
def privacy_policy():
    return render_template('privacy_policy.html')

@default_views.route('/licensing_agreement')
def licensing_agreement():
    return render_template('licensing_agreement.html')

@default_views.route('/about')
def about():
    return render_template('about.html')

