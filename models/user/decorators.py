from functools import wraps
from typing import Callable
from flask import session, flash, redirect, url_for, request, current_app

def requires_login(f: Callable) -> Callable:
  '''
  If you decorate a view with this, it will ensure that the current user is
  logged in with email and authenticated before calling the actual view.
  :param func: The view function to decorate.
  :type func: function
  '''
  @wraps(f)
  def decorated_function(*args, **kwargs):
    if not session.get('email'):
      flash('You need to be signed in to view this page.', 'danger')
      return redirect(url_for('users.login'))
    return f(*args, **kwargs)
  return decorated_function

def requires_admin(f: Callable) -> Callable:
  '''
  If you decorate a view with this, it will ensure that the current user is
  an admin user by checking the email in the config for ADMIN variable.
  :param func: The view function to decorate.
  :type func: function
  '''
  @wraps(f)
  def decorated_function(*args, **kwargs):
    if not session.get('email') != current_app.config.get('ADMIN', ''):
      flash('You need to be an admin to access this page.', 'danger')
      return redirect(url_for('users.login'))
    return f(*args, **kwargs)
  return decorated_function