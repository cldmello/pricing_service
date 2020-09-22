from flask import Flask, render_template
from views.items import item_blue
from views.alerts import alert_blue
from views.stores import store_blue
from views.users import user_blue
import os

app = Flask(__name__)
app.secret_key = os.urandom(64)
app.config.update(
  ADMIN=os.environ.get('ADMIN')
)

@app.route('/')
def home():
  return render_template('home.html')

# app.register_blueprint(item_blue, url_prefix='/items')
app.register_blueprint(alert_blue, url_prefix='/alerts')
app.register_blueprint(store_blue, url_prefix='/stores')
app.register_blueprint(user_blue, url_prefix='/users')

if __name__ == '__main__':
  app.run(debug=True)