DROP TABLE IF EXISTS brewery;
DROP TABLE IF EXISTS beer;
DROP TABLE IF EXISTS winery;
DROP TABLE IF EXISTS wine;
DROP VIEW IF EXISTS local_beers;
DROP TRIGGER IF EXISTS updateAbvBelowZero;
DROP TRIGGER IF EXISTS insertAbvBelowZero;

CREATE TABLE brewery (
  id INTEGER PRIMARY KEY NOT NULL,
  name TEXT NOT NULL,
  city TEXT,
  state TEXT,
  country TEXT,
  latitude FLOAT,
  longitude FLOAT
);

CREATE TABLE beer (
  id INTEGER PRIMARY KEY NOT NULL,
  name TEXT NOT NULL,
  brewery_id INTEGER,
  style TEXT,
  abv FLOAT,
  FOREIGN KEY(brewery_id) REFERENCES brewery(id)
);

CREATE TABLE winery (
  id INTEGER PRIMARY KEY NOT NULL,
  name TEXT NOT NULL,
  region TEXT,
  state TEXT,
  country TEXT,
  latitude FLOAT,
  longitude FLOAT,
  photo_url TEXT
);

CREATE TABLE wine (
  id INTEGER PRIMARY KEY NOT NULL,
  name TEXT NOT NULL,
  variety TEXT,
  photo_url TEXT,
  winery_id INTEGER,
  FOREIGN KEY(winery_id) REFERENCES winery(id)
);

CREATE TABLE wine_review (
  id INTEGER PRIMARY KEY NOT NULL,
  text TEXT NOT NULL,
  rating INTEGER,
  taster TEXT,
  taster_media TEXT,
  title TEXT,
  wine_id INTEGER,
  FOREIGN KEY(wine_id) REFERENCES wine(id)
);

CREATE TRIGGER updateAbvBelowZero AFTER UPDATE ON beer
FOR EACH ROW
  WHEN (NEW.abv IS NOT NULL AND NEW.abv < 0)
BEGIN
  UPDATE beer SET abv = NULL WHERE id = NEW.id;
END;

CREATE TRIGGER insertAbvBelowZero AFTER INSERT ON beer
FOR EACH ROW
  WHEN (NEW.abv IS NOT NULL AND NEW.abv < 0)
BEGIN
  UPDATE beer SET abv = NULL WHERE id = NEW.id;
END;

CREATE VIEW local_beers (
  id,
  brewery_id,
  name,
  style,
  abv,
  brewery_name,
  city,
  state
) AS
SELECT beer.id
     , beer.brewery_id
     , beer.name
     , beer.style
     , beer.abv
     , brewery.name
     , brewery.city
     , brewery.state
FROM Beer beer, Brewery brewery 
WHERE beer.brewery_id = brewery.id 
  AND (brewery.state = 'IL'
    OR brewery.state = 'illinois'
    OR brewery.state = 'Illinois')
;