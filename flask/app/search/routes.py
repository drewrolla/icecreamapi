import requests
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from .forms import IceCreamSearchForm
from app.models import Icecream, User, db
from .YelpAPI import API_KEY

search = Blueprint('search', __name__, template_folder='searchtemplates')

ENDPOINT = "https://api.yelp.com/v3/businesses/search"
API_AUTH = {'Authorization': 'bearer %s' % API_KEY}

@search.route('/search', methods=["GET", "POST"])
def searchIceCream():
    form = IceCreamSearchForm()
    my_dict = {}
    saved = False
    if request.method == "POST":
        print('Post request made.')
        if form.validate():
            location = form.location.data

            # Define the parameters
            PARAMETERS = {
                'location': location,
                'categories': 'icecream',
                'limit': 50,
                'radius': 10000
            }
            res = requests.get(url = ENDPOINT, params=PARAMETERS, headers=API_AUTH)
            if res.ok:
                yelp_data = res.json()
                for each in yelp_data['businesses']:
                    my_dict = {
                        'name': each['name'],
                        'rating': each['rating'],
                        'address': each['location']['address1'],
                        'img_url': each['image_url'],
                        'website': each['url']
                    }
                shops = Icecream.query.filter_by(name=my_dict['name']).first()
                if not shops:
                    shops = Icecream(my_dict['name'], my_dict['rating'], my_dict['address'], my_dict['img_url'], my_dict['website'])
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

@search.route('/saved', methods=["GET","POST"])
def savedShops():
    shops = current_user.shop.all()
    return render_template('savedshops.html', shops=shops)


######### API ##########
@search.route('/api/search', methods=["POST"])
def apiSearch():
    form = IceCreamSearchForm()
    my_dict = {}
    saved = False
    if request.method == "POST":
        print('Post request made.')
        if form.validate():
            location = form.location.data

            # Define the parameters
            PARAMETERS = {
                'location': location,
                'categories': 'icecream',
                'limit': 50,
                'radius': 10000
            }
            res = requests.get(url = ENDPOINT, params=PARAMETERS, headers=API_AUTH)
            if res.ok:
                yelp_data = res.json()
                for each in yelp_data['businesses']:
                    my_dict = {
                        'name': each['name'],
                        'rating': each['rating'],
                        'address': each['location']['address1'],
                        'img_url': each['image_url'],
                        'website': each['url']
                    }
                shops = Icecream.query.filter_by(name=my_dict['name']).first()
                if not shops:
                    shops = Icecream(my_dict['name'], my_dict['rating'], my_dict['address'], my_dict['img_url'], my_dict['website'])
                    shops.save()
                if current_user.shop.filter_by(name=shops.name).first():
                    saved = True
    return {
        'status': 'ok',
        'message': 'search completed!'
    }