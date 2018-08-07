# app/__init__.py

from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify, abort

# local import
from instance.config import app_config

# initialize sql-alchemy
db = SQLAlchemy()

def create_app(config_name):
    from app.models import ShoppingList, Item
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    
    @app.route('/shoppinglists/', methods=['POST', 'GET'])
    def shoppinglists():
        if request.method == "POST":
            title = str(request.data.get('title', ''))
            store = str(request.data.get('store', ''))
            if title and store:
                shoppinglist = ShoppingList(title=title, store=store)
                db.session.add(shoppinglist)
                db.session.commit()
                response = jsonify({
                    'id': shoppinglist.id,
                    'title': shoppinglist.title,
                    'store':shoppinglist.store,
                    'date_created': shoppinglist.date_created,
                    'date_modified': shoppinglist.date_modified
                })
                response.status_code = 201
                return response
            else:
                abort(400)
        else:
            # GET
            shoppinglists = ShoppingList.query.all()
            results = []
            for shoppinglist in shoppinglists:
                obj = {
                    'id': shoppinglist.id,
                    'title': shoppinglist.title,
                    'store':shoppinglist.store,
                    'date_created': shoppinglist.date_created,
                    'date_modified': shoppinglist.date_modified
                }
                results.append(obj)
            response = jsonify(results)
            response.status_code = 200
            return response

    @app.route('/shoppinglists/<int:id>', methods=['GET', 'PUT', 'DELETE'])
    def shoppinglist_manipulation(id, **kwargs):
        # retrieve the shoppinglist using its ID
        shoppinglist = ShoppingList.query.filter_by(id=id).first()
        if not shoppinglist:
            # Raise an HTTPException with a 404 not found status code
            abort(404)
        if request.method == 'DELETE':
            db.session.delete(shoppinglist)
            db.session.commit()
            return {
                "message": "shoppinglist {} deleted successfully".format(shoppinglist.id) 
            }, 200
        elif request.method == 'PUT':
            title = str(request.data.get('title', ''))
            store = str(request.data.get('store', ''))
            shoppinglist.title = title
            shoppinglist.store = store
            db.session.add(shoppinglist)
            db.session.commit()
            response = jsonify({
                'id': shoppinglist.id,
                'title': shoppinglist.title,
                'store':shoppinglist.store,
                'date_created': shoppinglist.date_created,
                'date_modified': shoppinglist.date_modified
            })
            response.status_code = 200
            return response
        else:
            # GET
            response = jsonify({
                'id': shoppinglist.id,
                'title': shoppinglist.title,
                'store':shoppinglist.store,
                'date_created': shoppinglist.date_created,
                'date_modified': shoppinglist.date_modified
            })
            response.status_code = 200
            return response

    @app.route('/shoppinglists/search/<string:title>', methods=['GET'])
    def shoppinglist_search(title):
        # retrieve shoppinglists that match the title
        shoppinglists = ShoppingList.query.filter(ShoppingList.title.ilike('%'+title+'%')).all()
        results = []
        for shoppinglist in shoppinglists:
            obj = {
                'id': shoppinglist.id,
                'title': shoppinglist.title,
                'store':shoppinglist.store,
                'date_created': shoppinglist.date_created,
                'date_modified': shoppinglist.date_modified
            }
            results.append(obj)
        response = jsonify(results)
        response.status_code = 200
        return response

    @app.route('/shoppinglists/<int:id>/items/', methods=['POST', 'GET'])
    def shoppinglistitems(id):
        if request.method == "POST":
            name = str(request.data.get('name', ''))
            quantity = int(request.data.get('quantity', ''))
            if name and quantity:
                item = Item.query.filter(Item.shoppinglist_id==id).filter(Item.name.ilike(name)).first()
                if item:
                    item.quantity += quantity
                else:
                    item = Item(name=name, quantity=quantity, shoppinglist_id=id)
                db.session.add(item)
                db.session.commit()
                response = jsonify({
                    'id': item.id,
                    'name': item.name,
                    'quantity':item.quantity,
                    'shoppinglist_id':item.shoppinglist_id
                })
                response.status_code = 201
                return response
            else:
                abort(400)
        else:
            # GET
            items = Item.query.filter_by(shoppinglist_id=id)
            results = []
            for item in items:
                obj = {
                    'id': item.id,
                    'name': item.name,
                    'quantity':item.quantity,
                    'shoppinglist_id':item.shoppinglist_id
                }
                results.append(obj)
            response = jsonify(results)
            response.status_code = 200
            return response

    @app.route('/shoppinglists/<int:lid>/items/<int:id>', methods=['GET', 'PUT', 'DELETE'])
    def shoppinglistitem_manipulation(lid, id, **kwargs):
        # retrieve the shoppinglist using its ID
        item = Item.query.filter_by(shoppinglist_id=lid).filter_by(id=id).first()
        if not item:
            # Raise an HTTPException with a 404 not found status code
            abort(404)
        if request.method == 'DELETE':
            db.session.delete(item)
            db.session.commit()
            return {
                "message": "shoppinglist item {} deleted successfully".format(item.id) 
            }, 200
        elif request.method == 'PUT':
            name = str(request.data.get('name', ''))
            quantity = int(request.data.get('quantity', ''))
            item.name = name
            item.quantity = quantity
            db.session.add(item)
            db.session.commit()
            response = jsonify({
                'id': item.id,
                'name': item.name,
                'quantity':item.quantity,
                'shoppinglist_id':shoppinglist_id
            })
            response.status_code = 200
            return response
        else:
            # GET
            response = jsonify({
                'id': item.id,
                'name': item.name,
                'quantity':item.quantity,
                'shoppinglist_id':shoppinglist_id
            })
            response.status_code = 200
            return response

    return app