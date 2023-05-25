from flask import Blueprint, redirect, render_template, url_for, request,jsonify, session,current_app
from forms import LoginForm, RegistrationForm
from flask_login import login_user, logout_user,current_user
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf.csrf import validate_csrf
# from app import oauth
from stripe_view import add_customer
from authlib.integrations.flask_client import OAuth

oauth=OAuth(current_app)

auth = Blueprint('auth',__name__)

google_default_password = "A4b48DkmVxBK6sC"
google=oauth.register(
    name='google',
    client_id='100984851928-uel2t01s878iik3fe0ug4i6ahfc9ju08.apps.googleusercontent.com',
    client_secret='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',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    client_kwargs={'scope': 'openid profile email'},
    jwks_uri="https://www.googleapis.com/oauth2/v3/certs"
)

def logged_in():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

@auth.route('/g_login')
def glogin():
    logged_in()
    google = oauth.create_client('google')
    redirect_uri = url_for('auth.callback', _external=True,_scheme='https')
    return oauth.google.authorize_redirect(redirect_uri)

@auth.route('/callback')
def callback():
    logged_in()
    try:
        google = oauth.create_client('google')
        token = google.authorize_access_token()
        resp = google.get('userinfo',token=token)
        user_info = resp.json()
        user = User.query.filter_by(email=user_info["email"]).first()
        customer_id = add_customer(user_info["email"],(User.query.count())+1)
        if not user:
            hashed_password = generate_password_hash(google_default_password, method='scrypt')
            user = User(
                email=user_info["email"],
                password=hashed_password,
                customer_id = customer_id
            )
            user.add()
        login_user(user, remember=True)
    except Exception as e:
        for key in list(session.keys()):
            session.pop(key)
        session.clear()
        return f"Error Occured:-{str(e)} click here to <a href='{url_for('default_views.home')}'>redirect</a> home"
    return redirect(url_for('default_views.home'))

@auth.route('/login', methods=['GET', 'POST'])
def login():
    logged_in()
    form = LoginForm()
    if request.method == "POST":
        data = request.get_json()
        try:
            validate_csrf(request.headers.get('X-CSRFToken'))
        except:
            return jsonify({'error': 'Invalid CSRF token.'}), 400
        email = data['email']
        password = data['password']
        remember = data['remember']
        user = User.query.filter_by(email=email).first()
        if user is None:
            return jsonify({'email': 'E-mail not found'}), 400
        if not check_password_hash(user.password, password):
            return jsonify({'password': 'Password Incorrect'}), 400
        login_user(user, remember=remember)
        redirect_url = url_for('index')
        return jsonify({'redirect': redirect_url})
    return render_template('login.html', form=form)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    logged_in()
    form = RegistrationForm()
    if request.method == "POST":
        data = request.get_json()
        try:
            validate_csrf(request.headers.get('X-CSRFToken'))
        except:
            return jsonify({'error': 'Invalid CSRF token.'}), 400
        email = data['email']
        password = data['password']
        confirm_password = data['confirm_password']
        if User.query.filter_by(email=email).first():
            return jsonify({'email': 'E-mail already exist'}), 400
        if password != confirm_password:
            return jsonify({'password': 'Password are not matching'}), 400
        customer_id = add_customer(form.email.data,(User.query.count())+1)
        hashed_password = generate_password_hash(password, method='scrypt')
        user = User(
            email=form.email.data,
            password=hashed_password,
            customer_id = customer_id
        )
        user.add()
        # Log in the user
        login_user(user)
        redirect_url = url_for('index')
        return jsonify({'redirect': redirect_url})

    return render_template('register.html', form=form)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('default_views.home'))