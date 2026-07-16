from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///items.db'
db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {'id':self.id, 'name':self.name, 'price':self.price}
    
with app.app_context():
    db.create_all()

@app.post('/items')
def create_item():
    data = request.json
    item = Item(name=data['name'], price=data['price'])
    db.session.add(item)
    db.session.commit()
    return jsonify(item.to_dict()), 201

@app.get('/items')
def get_items():
    items = Item.query.all()
    return jsonify([item.to_dict() for item in items])

@app.get('/items/<int:item_id>')
def get_item(item_id):
    item = Item.query.get(item_id)
    if item is None:
        return jsonify({'error':'Not Found'}), 404
    return jsonify(item.to_dict())

@app.put('/items/<int:item_id>')
def update_item(item_id):
    item = Item.query.get(item_id)
    if item is None:
        return jsonify({'error': 'Not Found'}), 404
    data = request.json
    item.name = data.get('name', item.name)
    item.price = data.get('price', item.price)
    db.session.commit()
    return jsonify(item.to_dict())

@app.delete('/items/<int:item_id>')
def delete_item(item_id):
    item = Item.query.get(item_id)
    if item is None:
        return jsonify({'error': 'Not Found'}), 404
    db.session.delete(item)
    db.session.commit()
    return '', 204


if __name__ == '__main__':
    app.run(debug=True)