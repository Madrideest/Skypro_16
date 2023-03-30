from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(200), nullable=False)
    last_name = db.Column(db.String(200), nullable=False)
    age = db.Column(db.Integer)
    email = db.Column(db.String, unique=True)
    role = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(200), unique=True)


class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(1000))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    address = db.Column(db.String(500))
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer,  db.ForeignKey("user.id"))
    executor_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    customer = db.relationship("User", foreign_keys=[customer_id])
    executor = db.relationship("User", foreign_keys=[executor_id])


class Offer(db.Model):
    __tablename__ = 'offer'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"))
    executor_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    order = relationship("Order")
    user = relationship("User")


@app.route('/users', methods=["GET"])
def get_users():
    users_list = User.query.all()

    users_resp = []
    for user in users_list:
        users_resp.append({'id': user.id,
                           'first_name': user.first_name,
                           'last_name': user.last_name,
                           'age': user.age,
                           'email': user.email,
                           'role': user.role,
                           'phone': user.phone})
    return jsonify(users_resp)


@app.route('/users/<int:sid>')
def get_user(sid: int):
    user = User.query.get(sid)

    if user is None:
        return "user not found"

    return jsonify({'id': user.id,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'age': user.age,
                    'email': user.email,
                    'role': user.role,
                    'phone': user.phone})


@app.route('/orders', methods=["GET"])
def get_orders():
    orders_list = Order.query.all()

    orders_resp = []
    for order in orders_list:
        orders_resp.append({'id': order.id,
                            'name': order.name,
                            'description': order.description,
                            'start_date': order.start_date,
                            'end_date': order.end_date,
                            'address': order.address,
                            'price': order.price,
                            'customer_id': order.customer_id,
                            'executor_id': order.executor_id})
    return jsonify(orders_resp)


@app.route('/orders/<int:sid>')
def get_order(sid: int):
    order = Order.query.get(sid)

    if order is None:
        return "order not found"

    return jsonify({'id': order.id,
                    'name': order.name,
                    'description': order.description,
                    'start_date': order.start_date,
                    'end_date': order.end_date,
                    'address': order.address,
                    'price': order.price,
                    'customer_id': order.customer_id,
                    'executor_id': order.executor_id})


@app.route('/offers', methods=["GET"])
def get_offers():
    offers_list = Offer.query.all()

    offers_resp = []
    for offer in offers_list:
        offers_resp.append({'id': offer.id,
                            'order_id': offer.order_id,
                            'executor_id': offer.executor_id})
    return jsonify(offers_resp)


@app.route('/offers/<int:sid>')
def get_offer(sid: int):
    offer = Offer.query.get(sid)

    if offer is None:
        return "offer not found"

    return jsonify({'id': offer.id,
                    'order_id': offer.order_id,
                    'executor_id': offer.executor_id})


@app.route('/users', methods=['POST'])
def create_user():
    user_data = request.get_json()
    user_add = User(
                    first_name=user_data['first_name'],
                    last_name=user_data['last_name'],
                    age=user_data['age'],
                    email=user_data['email'],
                    role=user_data['role'],
                    phone=user_data['phone']
                    )

    with db.session.begin():
        db.session.add(user_add)

    return 'User created successfully', 201


@app.route('/users/<int:sid>', methods=['PUT'])
def update_user(sid: int):
    user_data = request.get_json()
    user = User.query.get(sid)
    user.first_name = user_data['first_name']
    user.last_name = user_data['last_name']
    user.age = user_data['age']
    user.email = user_data['email']
    user.role = user_data['role']
    user.phone = user_data['phone']

    db.session.add(user)
    db.session.commit()

    return 'User updated successfully', 200


@app.route('/users/<int:sid>', methods=['DELETE'])
def delete_user(sid: int):
    user = User.query.get(sid)
    db.session.delete(user)
    db.session.commit()

    return 'User deleted successfully', 200


@app.route('/orders', methods=['POST'])
def create_order():
    orders_data = request.get_json()
    order_add = Order(
                    name=orders_data['name'],
                    description=orders_data['description'],
                    start_date=orders_data['start_date'],
                    end_date=orders_data['end_date'],
                    address=orders_data['address'],
                    price=orders_data['price'],
                    customer_id=orders_data['customer_id'],
                    executor_id=orders_data['executor_id']
                    )

    with db.session.begin():
        db.session.add(order_add)

    return 'order created successfully', 201


@app.route('/orders/<int:sid>', methods=['PUT'])
def update_order(sid: int):
    order_data = request.get_json()
    order = Order.query.get(sid)

    order.name = order_data['name'],
    order.description = order_data['description'],
    order.start_date = order_data['start_date'],
    order.end_date = order_data['end_date'],
    order.address = order_data['address'],
    order.price = order_data['price'],
    order.customer_id = order_data['customer_id'],
    order.executor_id = order_data['executor_id']

    db.session.add(order)
    db.session.commit()

    return 'order updated successfully', 200


@app.route('/orders/<int:sid>', methods=['DELETE'])
def delete_order(sid: int):
    order = Order.query.get(sid)
    db.session.delete(order)
    db.session.commit()

    return 'order deleted successfully', 200


@app.route('/offers', methods=['POST'])
def create_offer():
    offer_data = request.get_json()
    offer_add = Offer(
                    order_id=offer_data['order_id'],
                    executor_id=offer_data['executor_id']
                    )

    with db.session.begin():
        db.session.add(offer_add)

    return 'offer created successfully', 201


@app.route('/offers/<int:sid>', methods=['PUT'])
def update_offer(sid: int):
    offer_data = request.get_json()
    offer = Offer.query.get(sid)

    offer.order_id = offer_data['order_id']
    offer.executor_id = offer_data['executor_id']

    db.session.add(offer)
    db.session.commit()

    return 'offer updated successfully', 200


@app.route('/offers/<int:sid>', methods=['DELETE'])
def delete_offer(sid: int):
    offer = Offer.query.get(sid)
    db.session.delete(offer)
    db.session.commit()

    return 'offer deleted successfully', 200


if __name__ == '__main__':
    app.run(debug=True)
