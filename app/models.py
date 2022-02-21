from app import db, login
from flask_login import UserMixin # This is just for the User model!
from datetime import datetime as dt

class Cart(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), primary_key=True)

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    email = db.Column(db.String(150), index=True, unique=True)
    password = db.Column(db.String(200))
    created_on = db.Column(db.DateTime, default = dt.utcnow)
    shop = db.relationship(
        'Item',
        secondary = 'cart',
        backref=db.backref('users',lazy='dynamic'),
        lazy='dynamic'
    )
    is_admin = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f'<User: {self.id} | {self.email}>'

    def from_dict(self, data):
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']

    def add_to_cart(self, obj):
        self.shop.append(obj)
        self.save()
    
    def sum_cart(self):
        sum=0
        for obj in self.shop:
            item = Item.query.get(obj.id)
            sum += item.price
        return sum

    # saves the user to the database
    def save(self):
        db.session.add(self) # add the user to the db session
        db.session.commit() #save everything in the session to the database

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
    # SELECT * FROM user WHERE id = ???

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.Text)
    price = db.Column(db.Float)
    date_created = db.Column(db.DateTime, default=dt.utcnow)

    def __repr__(self):
        return f'<Post: {self.id} | {self.body[:15]}>'


    def to_dict(self):
        return {
            'id':self.id,
            'name':self.name,
            'description':self.description,
            'price':self.price,
            'date_created':self.date_created,
        }

    def edit(self, new_body):
        self.body = new_body
        self.save()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    # saves the post to the database
    def save(self):
        db.session.add(self) # add the user to the db session
        db.session.commit() #save everything in the session to the database

