from flask import Blueprint, request, abort, jsonify, render_template
from ..db import queryDB

def queryBeerByID(beer_id):
    query = '''SELECT beer.name
                    , beer.style
                    , beer.abv
                    , brewery.name   AS brewery_name
                    , brewery.city
                    , brewery.state
                    , beer.id
                    , beer.brewery_id
            FROM Beer beer, Brewery brewery 
            WHERE beer.brewery_id = brewery.id 
                AND beer.id = ?'''
    return queryDB(query, (beer_id,))

beers = Blueprint('beers', __name__,
                        template_folder='templates')

@beers.route('')
def get_beers():
    query = '''SELECT * FROM Beer ORDER BY RANDOM() LIMIT 500'''
    beers = queryDB(query)            
    if len(beers) == 0:
        abort(404)
    return jsonify({
    'success': True,
    'beers': beers
    })

@beers.route('/search', methods=['POST'])
def search_beers():
    searchName = request.form['name']
    if len(searchName) == 0:
        query = '''SELECT beer.id
                        , beer.brewery_id
                        , beer.name
                        , beer.style
                        , beer.abv
                        , brewery.name
                        , brewery.city
                        , brewery.state
                    FROM Beer beer, Brewery brewery
                    WHERE beer.brewery_id = brewery.id
                    ORDER BY RANDOM()
                    LIMIT 500'''
        beers = queryDB(query)
    else:
        query = '''SELECT beer.id
                        , beer.brewery_id
                        , beer.name
                        , beer.style
                        , beer.abv
                        , brewery.name
                        , brewery.city
                        , brewery.state
                    FROM Beer beer, Brewery brewery 
                    WHERE beer.brewery_id = brewery.id
                        AND beer.name LIKE ? 
                    ORDER BY RANDOM()
                    LIMIT 500'''
        query_params = ('%'+searchName+'%',)
        beers = queryDB(query, query_params)

    if len(beers) == 0:
        abort(404)

    return render_template("searchBeer.html", data=beers)

@beers.route('/<int:beer_id>', methods=['GET'])
def get_beer(beer_id):
    beer = queryBeerByID(beer_id)
    if len(beer) == 0:
        abort(404)
    return render_template("updateBeer.html", data=beer_id)

@beers.route('/delete/<int:beer_id>', methods=['POST'])
def delete_beer(beer_id):
    query = '''DELETE FROM beer WHERE id = ?'''
    query_params = (beer_id,)
    try:
        queryDB(query, query_params)
        return jsonify({
            'success': True,
            'deleted': beer_id
        })

    except Exception:
        abort(422)

@beers.route('', methods=['POST'])
def create_beer():
    data = request.form
    name = data.get('name') or None
    style = data.get('style') or None
    brewery_name = data.get('brewery') or None
    abv = data.get('alcoholContent') or None
    city = data.get('city') or None
    state = data.get('state') or None

    try:
        existing_beer = '''SELECT *
                            FROM beer
                            WHERE name = ?
                            AND style = ?
                            '''
        beer_params = (name, style,)
        existing_data = queryDB(existing_beer,beer_params)

        if len(existing_data) == 0:
            existing_brewery = '''SELECT id
                            FROM brewery
                            WHERE name = ?
                                AND city = ?
                                AND state = ?
                            '''
            brewery_params = (brewery_name, city, state,)
            existing_data = queryDB(existing_brewery, brewery_params)
            if len(existing_data) > 0:
                brewery_id = existing_data[0][0]
            else:
                id_query = '''SELECT MAX(id) AS max_id FROM brewery'''
                brewery_id = queryDB(id_query)[0][0] + 1
                
                query = '''INSERT INTO brewery (id, name, city, state, country)
                                        VALUES (?,?,?,?,?)
                                        '''
                params = (brewery_id, brewery_name, city, state, 'US',)
                queryDB(query,params)

            id_query = '''SELECT MAX(id) AS max_id FROM beer'''
            new_beer_id = queryDB(id_query)[0][0] + 1
            query = '''INSERT INTO beer (id, name, style, abv, brewery_id)
                                VALUES (?,?,?,?,?)
                                '''
            params = (new_beer_id, name, style, abv, brewery_id,)
            queryDB(query,params)

        return jsonify({
            'success': True,
            'created': new_beer_id
        })
    except Exception:
        abort(422)

@beers.route('/<int:beer_id>', methods=['POST'])
def edit_beer(beer_id):
    existing_data = queryBeerByID(beer_id)
    data = request.form

    try:
        name = data.get('name')
        style = data.get('style')
        abv = data.get('alcoholContent')
        if name or style or abv:
            if len(name) == 0:
                name = existing_data[0][0]
            if len(style) == 0:
                style = existing_data[0][1]
            if len(abv) == 0:
                abv = existing_data[0][2]
            query = '''UPDATE beer 
                        SET name = ?, 
                            style = ?, 
                            abv = ? 
                            WHERE id = ?'''
            params = (name, style, abv, beer_id,)
            queryDB(query,params)

        brewery_id = existing_data[0][7]
        brewery_name = data.get('brewery_name')
        city = data.get('city')
        state = data.get('state')
        if brewery_name or city or state:
            if len(brewery_name) == 0:
                brewery_name = existing_data[0][3]
            if len(city) == 0:
                city = existing_data[0][4]
            if len(state) == 0:
                state = existing_data[0][5]
            query = '''UPDATE brewery SET name = ?, 
                            city = ?, 
                            state = ? 
                            WHERE id = ?'''
            params = (brewery_name, city, state, brewery_id,)
            queryDB(query,params)

        return jsonify({
                    'success': True,
                    'updated': beer_id
                })
    except Exception:
        abort(422)

@beers.route('/<int:beer_id>/reviews', methods=['GET'])
def get_beer_reviews(beer_id):
    query = '''SELECT * FROM beer 
                    WHERE id = ?'''
    param = (beer_id,)
    name = queryDB(query, param)[0][1]
    reviews = beerReviews.query(KeyConditionExpression=Key('beer_id').eq(beer_id))['Items']
    return render_template("beerReviews.html", data={
        'id': beer_id,
        'name': name,
        'reviews': reviews})

@beers.route('/<int:beer_id>/reviews/add')
def addBeerReview(beer_id):
    return render_template("addBeerReviews.html", id=beer_id)

@beers.route('/<int:beer_id>/reviews', methods=['POST'])
def add_beer_review(beer_id):
    data = request.form
    review = {}
    review['beer_id'] = beer_id
    review['username'] = data.get('username')
    review['date'] = date.today().strftime("%Y-%m-%d")
    attributes = ['text', 'taste', 'smell', 'look', 'feel', 'overall']
    for attribute in attributes:
        if data.get(attribute):
            review[attribute] = data.get(attribute)
    try:
        beerReviews.put_item(Item=review)
        return jsonify({
            'success': True
        })

    except Exception:
        abort(422)