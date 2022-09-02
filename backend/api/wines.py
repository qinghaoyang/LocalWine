from operator import or_
from flask import Blueprint, request, abort, jsonify, render_template

from backend.models.wine_reviews import WineReview
from ..db import queryDB
from backend.models.wines import Wine
from backend.api.errorhandlers import errs

def queryWineByID(wine_id):
    query = '''SELECT wine.name
                    , wine.variety
                    , wine.rating
                    , winery.name  AS winery_name 
                    , winery.city
                    , winery.state
                    , wine.id
                    , wine.winery_id
            FROM Wine wine, Winery winery
            WHERE wine.winery_id = winery.id 
                AND wine.id = ?'''
    return queryDB(query, (wine_id,))

wines = Blueprint('wines', __name__,
                        template_folder='templates')

@wines.route('')
def get_wines():
    query = '''SELECT * FROM Wine ORDER BY RANDOM() LIMIT 500'''
    wines = queryDB(query)            
    if len(wines) == 0:
        abort(404)
    return jsonify({
    'success': True,
    'wines': wines
    })

@wines.route('/search', methods=['POST'])
def search_wines():
    searched_text = request.json['searched_text']
    if len(searched_text) == 0:
        wines = Wine.query.all()
    else:
        wines = Wine.query.filter(
            or_(
                Wine.name.ilike('%' + searched_text + '%'),
                Wine.variety.ilike('%' + searched_text + '%')
            )
        ).all()

    if len(wines) == 0:
        abort(404)

    return jsonify({
        'success': True,
        'wines': [wine.format() for wine in wines]
    })

@wines.route('/<int:wine_id>', methods=['GET'])
def get_wine(wine_id):
    wine = Wine.query.filter_by(id=wine_id).first()
    if not wine:
        abort(404)

    return jsonify({
        'success': True,
        'wine': wine.format()
    })

@wines.route('/delete/<int:wine_id>', methods=['POST'])
def delete_wine(wine_id):
    query = '''DELETE FROM wine WHERE id = ?'''
    query_params = (wine_id,)
    try:
        queryDB(query, query_params)
        return jsonify({
            'success': True,
            'deleted': wine_id
        })

    except Exception:
        abort(422)

@wines.route('', methods=['POST'])
def create_wine():
    data = request.form
    name = data.get('name') or None
    variety = data.get('variety') or None
    winery_name = data.get('winery') or None
    rating = data.get('rating') or None
    city = data.get('city') or None
    state = data.get('state') or None

    try:
        existing_wine = '''SELECT *
                            FROM wine
                            WHERE name = ?
                            AND variety = ?
                            '''
        wine_params = (name, variety,)
        existing_data = queryDB(existing_wine,wine_params)

        if len(existing_data) == 0:
            existing_winery = '''SELECT id
                            FROM winery
                            WHERE wname = ?
                                AND city = ?
                                AND state = ?
                            '''
            winery_params = (winery_name, city, state,)
            existing_data = queryDB(existing_winery, winery_params)
            if len(existing_data) > 0:
                winery_id = existing_data[0][0]
            else:
                id_query = '''SELECT MAX(id) AS max_id FROM winery'''
                winery_id = queryDB(id_query)[0][0] + 1
                
                query = '''INSERT INTO winery (id, name, city, state, country)
                                        VALUES (?,?,?,?,?)
                                        '''
                params = (winery_id, winery_name, city, state, 'US',)
                queryDB(query,params)

            id_query = '''SELECT MAX(id) AS max_id FROM wine'''
            new_wine_id = queryDB(id_query)[0][0] + 1
            query = '''INSERT INTO wine (id, name, variety, rating, winery_id)
                                VALUES (?,?,?,?,?)
                                '''
            params = (new_wine_id, name, variety, rating, winery_id,)
            queryDB(query,params)

        return jsonify({
            'success': True,
            'created': new_wine_id
        })
    except Exception:
        abort(422)

@wines.route('/<int:wine_id>', methods=['POST'])
def edit_wine(wine_id):
    existing_data = queryWineByID(wine_id)
    data = request.form

    name = data.get('name')
    variety = data.get('variety')
    rating = data.get('rating')
    if name or variety or rating:
        if len(name) == 0:
            name = existing_data[0][0]
        if len(variety) == 0:
            variety = existing_data[0][1]
        if len(rating) == 0:
            rating = existing_data[0][2]
        query = '''UPDATE wine SET name = ?, 
                        variety = ?, 
                        rating = ? 
                        WHERE id = ?'''
        params = (name, variety, rating, wine_id,)
        queryDB(query,params)

    winery_id = existing_data[0][7]
    winery_name = data.get('winery_name')
    city = data.get('city')
    state = data.get('state')
    if winery_name or city or state:
        if len(winery_name) == 0:
            winery_name = existing_data[0][3]
        if len(city) == 0:
            city = existing_data[0][4]
        if len(state) == 0:
            state = existing_data[0][5]
        query = '''UPDATE winery SET name = ?, 
                            city = ?, 
                            state = ? 
                            WHERE id = ?'''
        params = (winery_name, city, state, winery_id,)
        queryDB(query,params)

    return jsonify({
        'success': True,
        'updated': winery_id
    })

@wines.route('/<int:wine_id>/reviews', methods=['GET'])
def get_wine_reviews(wine_id):
    wine = Wine.query.filter_by(id=wine_id).first()
    if not wine:
        abort(404)

    formatted_reviews = [review.format() for review in wine.reviews]
    ratings = [review['rating'] for review in formatted_reviews]
    avg_rating = sum(ratings) / len(ratings)
    return jsonify({
        'success': True,
        'reviews': formatted_reviews,
        'avg_rating': avg_rating
    })

@wines.route('/<int:wine_id>/reviews', methods=['POST'])
def add_wine_review(wine_id):
    taster = request.json['taster']
    rating = request.json['rating']
    text = request.json['text']
    wine_review = WineReview(rating=rating, text=text, wine_id=wine_id, taster=taster)

    try:
        wine = Wine.query.filter_by(id=wine_id).first()
        wine.reviews.append(wine_review)
        wine_review.insert()
        return jsonify({
            'success': True,
            'created': wine_review.id
        })
    
    except Exception:
        abort(422)