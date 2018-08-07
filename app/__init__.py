# app/__init__.py

from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify, abort

# local import
from instance.config import app_config

# initialize sql-alchemy
db = SQLAlchemy()

def create_app(config_name):
    from app.models import ShoppingList
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
        # retrieve a shoppinglist using its ID
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

    return app