import os
from flask import Flask
from flask_cors import CORS

from backend.models import database
from backend.api.errorhandlers import errs
from backend.api.wineries import wineries
from backend.api.wines import wines

def create_app(test_config=None):
    # create and configure the app
    app = Flask(
        __name__,
        static_folder='templates/src',
        template_folder='templates/public',
        instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        'sqlite:///' + os.path.join(app.instance_path, 'flaskr.sqlite'))
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    database.app = app
    database.init_app(app)

    app.register_blueprint(errs)
    app.register_blueprint(wineries, url_prefix='/wineries')
    app.register_blueprint(wines, url_prefix='/wines')
    CORS(app)

    # boto_sess = Session(
    # region_name='us-east-2',
    # aws_access_key_id='',
    # aws_secret_access_key=''
    # )

    # app.config['DYNAMO_SESSION'] = boto_sess
    # dynamo = Dynamo()
    # dynamo.init_app(app)
    # beerReviews = dynamo.tables['beerReviews']
    # wineReviews = dynamo.tables['wineReviews']

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # @app.route("/")
    # def home():
    #     return jsonify({'home': 'home'})

    # @app.route("/addBeer")
    # def addBeer():
    #     return render_template("addBeer.html")

    # @app.route("/searchBeer")
    # def searchBeer():
    #     return render_template("searchBeer.html", data=[])

    # @app.route("/addWine")
    # def addWine():
    #     return render_template("addWine.html")

    # @app.route("/searchWine")
    # def searchWine():
    #     return render_template("searchWine.html", data=[])

    # @app.route('/localbeers')
    # def localBeers():
    #     query = '''SELECT *
    #                 FROM local_beers
    #                 LIMIT 500'''
    #     local_beers = queryDB(query)
    #     if len(local_beers) == 0:
    #         abort(404)

    #     return render_template("pages/localBeers.html", data=local_beers)

    # @app.route('/heatmap')
    # def heatMap():
    #     map = folium.Map(location=[38, -98], zoom_start=5)
    #     locations = getLocations()
    #     address_latlng = []
    #     for location in locations:
    #         address = geocoder.osm(location[0] + ', ' + location[1])
    #         if address.lat and address.lng:
    #             address_latlng.append([address.lat, address.lng])
    #     HeatMap(address_latlng).add_to(map)
    #     return map._repr_html_()

    # def getLocations():
    #     query = '''SELECT city
    #                     , state
    #                 FROM brewery
    #                 UNION ALL
    #                 SELECT city
    #                     , state
    #                 FROM winery
    #                 LIMIT 100'''
    #     locations = queryDB(query)
    #     return locations

    from . import db
    db.init_app(app)

    return app