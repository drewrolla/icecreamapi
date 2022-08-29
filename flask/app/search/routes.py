import requests
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from .forms import IceCreamSearchForm
from app.models import Icecream, User, db

search = Blueprint('search', __name__, template_folder='searchtemplates')

@search.route('/search', methods=["GET", "POST"])
def searchIceCream():
    form = IceCreamSearchForm()
    my_dict = {}
    saved = False
    if request.method == "POST":
        print('Post request made.')
        if form.validate():
            location = form.location.data
            url = f"https://api.yelp.com/v3/businesses/{location}"
            res = requests.get(url)
            if res.ok:
                data = res.json()
                my_dict = {
                    'name': data['businesses']['name'],
                    'rating': data['businesses']['rating'],
                    'price': data['businesses']['price'],
                    'address': data['businesses']['location'][5],
                    'img_url': data['businesses']['image_url'],
                    'website': data['businesses']['url']
                }
                shops = Icecream.query.filter_by(name=my_dict['name']).first()
                if not shops:
                    shops = Icecream(my_dict['name'], my_dict['rating'], my_dict['price'], my_dict['address'], my_dict['img_url'], my_dict['website'])
                    shops.save()
                if current_user.shop.filter_by(name=shops.name).first():
                    saved = True
    return render_template('icecreamsearch.html', form=form, shops=my_dict, saved=saved)


# save ice cream shops
@search.route('/save/<string:icecream_name>')
def saveIceCream(icecream_name):
    current_user
    shops = Icecream.query.filter_by(name=icecream_name).first()
    current_user.shop.append(shops)
    db.session.commit()
    return redirect(url_for('search.searchIceCream'))

# remove
@search.route('/remove/<string:icecream_name>')
def removeIceCream(icecream_name):
    shops = Icecream.query.filter_by(name=icecream_name).first()
    current_user.shop.remove(shops)
    db.session.commit()
    return redirect(url_for('search.searchIceCream'))