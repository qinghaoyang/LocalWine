from backend.models import database

class WineReview(database.Model):
    __tablename__ = 'wine_review'

    id = database.Column(database.Integer, primary_key=True)
    text = database.Column(database.String, nullable=False)
    title = database.Column(database.String)
    rating = database.Column(database.Integer)
    taster = database.Column(database.String)
    taster_media = database.Column(database.String)
    wine_id = database.Column(database.Integer, database.ForeignKey('wine.id'))

    def __init__(
        self, text, rating, wine_id, title=None, taster=None, taster_media=None):
        self.text = text
        self.title = title
        self.rating = rating
        self.taster = taster
        self.taster_media = taster_media
        self.wine_id = wine_id

    def insert(self):
        database.session.add(self)
        database.session.commit()

    def update(self):
        database.session.commit()

    def delete(self):
        database.session.delete(self)
        database.session.commit()

    def format(self):
        return {
            'id': self.id,
            'text': self.text,
            'title': self.title,
            'rating': self.rating,
            'taster': self.taster,
            'taster_media': self.taster_media,
            'wine_id': self.wine_id
        }