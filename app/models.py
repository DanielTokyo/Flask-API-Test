# app/models.py

from app import db

class ShoppingList(db.Model):
    """This class represents the shoppinglist table."""

    __tablename__ = 'shoppinglists'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    store = db.Column(db.String(255))
    items = db.relationship("Item", lazy='dynamic')
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())

    def __init__(self, title, store):
        """initialize with title and store."""
        self.title = title
        self.store = store

    def __repr__(self):
        return "<ShoppingList: {}>".format(self.title)
    
    def to_json(self):
        return dict(
            id=self.id, 
            title=self.title, 
            store=self.store,
            items=self.items.to_json(),
            date_created=self.date_created,
            date_modified=self.date_modified)

class Item(db.Model):
    """This class represents the shoppinglist item table."""

    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    quantity = db.Column(db.Integer)
    shoppinglist_id = db.Column(db.Integer, db.ForeignKey('shoppinglists.id'))
    shoppinglist = db.relationship("ShoppingList")

    def __init__(self, name, quantity, shoppinglist_id):
        """initialize with name and quantity."""
        self.name = name
        self.quantity = quantity
        self.shoppinglist_id = shoppinglist_id

    def __repr__(self):
        return "<Item: {}>".format(self.name)

    def to_json(self):
        return dict(
            id=self.id, 
            name=self.name, 
            quantity=self.quantity, 
            shopping_list_id=self.shoppinglist_id)