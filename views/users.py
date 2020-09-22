from flask import Blueprint, session, render_template, url_for, request, redirect
from models.user import User, UserErrors

user_blue = Blueprint('users', __name__)

@user_blue.route('/register', methods=['POST', 'GET'])
def register():
  if request.method == 'POST':
    email = request.form['email']
    password = request.form['password']

    try:
      User.register_user(email, password)
      session['email'] = email
      return email
    except UserErrors.UserError as e:
      return e.message

  return render_template('users/register.html')

@user_blue.route('/login', methods=['POST', 'GET'])
def login():
  if request.method == 'POST':
    email = request.form['email']
    password = request.form['password']

    try:
      if User.is_login_valid(email, password):
        session['email'] = email
        return email
    except UserErrors.UserError as e:
      return e.message

  return render_template('users/login.html')