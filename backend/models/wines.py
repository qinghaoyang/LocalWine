from backend.models import database
from backend.models.wine_reviews import WineReview

class Wine(database.Model):
    __tablename__ = 'wine'

    id = database.Column(database.Integer, primary_key=True, nullable=False)
    name = database.Column(database.String, nullable=False)
    variety = database.Column(database.String)
    photo_url = database.Column(database.String)
    winery_id = database.Column(database.Integer, database.ForeignKey('winery.id'))
    winery = database.relationship('Winery', backref='winery', lazy=True)
    reviews = database.relationship('WineReview', backref='wine_review', lazy=True)

    def __init__(self, id, name, variety, photo_url,winery_id):
        self.id = id
        self.name = name
        self.variety = variety
        self.photo_url = photo_url
        self.winery_id = winery_id

    def insert(self):
        database.session.add(self)
        database.session.commit()

    def update(self):
        database.session.commit()

    def delete(self):
        database.session.delete(self)
        database.session.commit()

    def format(self):
        reviews = self.reviews
        ratings = [review.rating for review in reviews]
        avg_rating = sum(ratings) / len(ratings) if len(ratings) > 0 else 0
        return {
            'id': self.id,
            'name': self.name,
            'variety': self.variety,
            'photo_url': self.photo_url,
            'winery_id': self.winery_id,
            'winery': self.winery.format(),
            'avg_rating': round(avg_rating, 1),
            'reviews': [review.format() for review in reviews]
        }