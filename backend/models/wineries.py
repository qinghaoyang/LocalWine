from backend.models import database

class Winery(database.Model):
    __tablename__ = 'winery'

    id = database.Column(database.Integer, primary_key=True, nullable=False)
    name = database.Column(database.String, nullable=False)
    region = database.Column(database.String)
    state = database.Column(database.String)
    country = database.Column(database.String)
    latitude = database.Column(database.Float)
    longitude = database.Column(database.Float)
    photo_url = database.Column(database.String)
    wines = database.relationship('Wine', backref='wine', lazy=True)

    def __init__(
            self, id, name, region, state,
            country, latitude, longitude, photo_url):
        self.id = id
        self.name = name
        self.region = region
        self.state = state
        self.country = country
        self.latitude = latitude
        self.longitude = longitude
        self.photo_url = photo_url

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
            'name': self.name,
            'region': self.region,
            'state': self.state,
            'country': self.country,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'photo_url': self.photo_url
        }