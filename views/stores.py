import json
from flask import Blueprint, render_template, url_for, request, redirect
from models.store import Store
from models.user import requires_login, requires_admin

store_blue = Blueprint('stores', __name__)

@store_blue.route('/')
@requires_login
def index():
  stores = Store.all()
  return render_template('stores/index.html', stores=stores)

@store_blue.route('/new', methods=['POST', 'GET'])
@requires_admin
def new_store():
  if request.method == 'POST':
    name = request.form['name']
    url_prefix = request.form['url_prefix']
    tag = request.form['tag']
    query = request.form['query']

    Store(name, url_prefix, tag, query).save_to_mongo()

  return render_template('stores/new_store.html')

@store_blue.route('/edit/<string:store_id>', methods=['POST', 'GET'])
@requires_admin
def edit_store(store_id):
  store = store.get_by_id(store_id)

  if request.method == 'POST':
    name = request.form['name']
    url_prefix = request.form['url_prefix']
    tag = request.form['tag']
    query = json.loads(request.form['query'])
    store.name = name
    store.url_prefix = url_prefix
    store.tag = tag
    store.query = query
    store.save_to_mongo()

    return redirect(url_for('.index'))

  return render_template('stores/edit_store.html', store=store)

@store_blue.route('/delete/<string:store_id>')
def delete_store(store_id):
  Store.get_by_id(store_id).remove_from_mongo()
  return redirect(url_for('.index'))