from flask import Blueprint, abort, jsonify
from backend.models.wineries import Winery

wineries = Blueprint('wineries', __name__,
                        template_folder='templates')

@wineries.route('/<country>')
def get_wineries_by_country(country):
    wineries = Winery.query.filter_by(country=country).all()
    if len(wineries) == 0:
        abort(404)

    formatted_wineries = [winery.format() for winery in wineries]
    return jsonify({
        'success': True,
        'wineries': formatted_wineries
    })

@wineries.route('/US/<state>')
def get_wineries_by_state(state):
    wines = Winery.query.filter_by(state=state).all()
    if len(wines) == 0:
        abort(404)

    formatted_wineries = [winery.format() for winery in wineries]
    return jsonify({
        'success': True,
        'wineries': formatted_wineries
    })

@wineries.route('/<int:winery_id>/wines')
def get_wines_by_winery_id(winery_id):
    winery = Winery.query.filter_by(id=winery_id).first()
    if not winery:
        abort(404)

    formatted_wines = [wine.format() for wine in winery.wines]
    return jsonify({
        'success': True,
        'wines': formatted_wines
    })