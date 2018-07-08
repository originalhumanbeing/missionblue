from flask import Flask, request
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime, func
from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///missionblue.sqlite3'
db = SQLAlchemy(app)

corals = []
fishes = []


class Coral(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    created = db.Column(DateTime(timezone=True))
    modified = db.Column(DateTime(timezone=True))
    name = db.Column(db.String(100))
    habitat = db.Column(db.String(100))
    shape = db.Column(db.String(200))
    color = db.Column(db.String(50))
    size = db.Column(db.String(10))
    characters = db.Column(db.String(100))

    def __init__(self, name, habitat, shape, color, size, characters):
        self.name = name
        self.habitat = habitat
        self.shape = shape
        self.color = color
        self.size = size
        self.characters = characters


class Fish(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    created = db.Column(DateTime(timezone=True))
    modified = db.Column(DateTime(timezone=True))
    name = db.Column(db.String(100))
    habitat = db.Column(db.String(100))
    pattern = db.Column(db.String(200))
    color = db.Column(db.String(50))
    size = db.Column(db.String(10))
    characters = db.Column(db.String(100))

    def __init__(self, name, habitat, pattern, color, size, characters):
        self.name = name
        self.habitat = habitat
        self.pattern = pattern
        self.color = color
        self.size = size
        self.characters = characters


db.create_all()


class FishResource(Resource):
    def get(self, name):
        for fish in fishes:
            if fish['name'] == name:
                return fish
        return {'fish': None}, 404

    def post(self, name):
        req = request.get_json()
        # fish = {'name': name,
        #         'habitat': req['habitat'],
        #         'pattern': req['pattern'],
        #         'color': req['color'],
        #         'size': req['size'],
        #         'character': req['character']
        #         }
        habitat = req['habitat']
        pattern = req['pattern']
        color = req['color']
        size = req['size']
        character = req['character']

        f = Fish(name=name, habitat=habitat, pattern=pattern, color=color, size=size, characters=character)
        db.session.add(f)
        db.session.commit()

        # fishes.append(fish)
        return req, 201

    def patch(self, name):
        req = request.get_json()
        new_fish = {'name': name,
                    'habitat': req['habitat'],
                    'pattern': req['pattern'],
                    'color': req['color'],
                    'size': req['size'],
                    'character': req['character']
                    }

        for fish in fishes:
            if name == fish['name']:
                fishes.remove(fish)
                fishes.append(new_fish)
                return new_fish, 201

    def delete(self, name):
        for fish in fishes:
            if fish['name'] == name:
                fishes.remove(fish)
                return fish, 200
            return {'fish': None}, 404


class FishesResource(Resource):
    def get(self):
        fishes = db.session.query(Fish).all()
        return str(len(fishes)), 200


class CoralResource(Resource):
    def get(self, name):
        for coral in corals:
            if coral['name'] == name:
                return coral, 200
        return {'coral': None}, 404

    def post(self, name):
        req = request.get_json()
        coral = {'name': name,
                 'habitat': req['habitat'],
                 'shape': req['shape'],
                 'color': req['color'],
                 'size': req['size'],
                 'character': req['character']
                 }
        corals.append(coral)
        return coral, 201

    def patch(self, name):
        req = request.get_json()
        new_coral = {'name': name,
                     'habitat': req['habitat'],
                     'shape': req['shape'],
                     'color': req['color'],
                     'size': req['size'],
                     'character': req['character']
                     }

        for coral in corals:
            if name == coral['name']:
                corals.remove(coral)
                corals.append(new_coral)
                return new_coral, 201

    def delete(self, name):
        for coral in corals:
            if name == coral['name']:
                corals.remove(coral)
                return coral, 200
            return {'coral': None}, 404


class CoralsResource(Resource):
    def get(self):
        return corals, 200


api.add_resource(FishResource,
                 '/fish/<string:name>')

api.add_resource(FishesResource,
                 '/fishes')

api.add_resource(CoralResource,
                 '/coral/<string:name>')

api.add_resource(CoralsResource,
                 '/corals')

if __name__ == '__main__':
    app.run(debug=True)
