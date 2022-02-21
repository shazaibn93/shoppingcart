from .import bp as shop
from flask import render_template, flash, redirect, url_for, request
from app.models import User, Item, Cart
from flask_login import login_required, current_user

@shop.route('/', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('index.html.j2')

@shop.route('/inventory', methods=['GET', 'POST'])
@login_required
def show_inventory():
    ## Find all our items that we sell
    items=Item.query.all()
    return render_template('inventory.html.j2', items=items)


@shop.route('/cart', methods=['GET', 'POST'])
@login_required
def my_cart():
    # get all the items user has added to their cart
    cart_items = current_user.shop
    return render_template('cart.html.j2',cart_items=cart_items)

@shop.route('/item/<int:id>', methods=['GET', 'POST'])
@login_required
def get_item(id):
    item = Item.query.get(id)
    return render_template('single_item.html.j2', item=item, view_all=True)

@shop.route('/add_item/<int:id>', methods=['GET', 'POST'])
@login_required
def add_item(id):
    user = current_user
    item = Item.query.get(id)
    user.add_to_cart(item)
    return render_template('cart.html.j2', cart_items=user.shop)

@shop.route('/remove_item/<int:id>', methods=['GET', 'POST'])
@login_required
def remove_item(id):
    deleted = Cart.query.get((current_user.id,id))
    if deleted:
        deleted.delete()
        flash(f'You have removed item {id} from cart', 'warning')
    return render_template('cart.html.j2', cart_items=current_user.shop)

@shop.route('/clear_cart', methods=['GET', 'POST'])
@login_required
def clear_cart():
    deleted = Cart.query.filter_by(user_id=current_user.id).all()
    if deleted:
        for i in deleted:
            i.delete()
            flash(f'You have removed item {id} from cart', 'warning')
    return render_template('cart.html.j2', cart_items=current_user.shop)
