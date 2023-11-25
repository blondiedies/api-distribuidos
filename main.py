from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_swagger import swagger
from flask_swagger_ui import get_swaggerui_blueprint
import json

app = Flask(__name__)
api = Api(app)

def read_json():
    with open('./venv/data.json', 'r') as f:
        data = json.load(f)
    return data

def write_json(data):
    with open('./venv/data.json', 'w') as f:
        json.dump(data, f)

class Status(Resource):
    def get(self):
        """
        Return the status of the API
        ---
        tags:
            - status
        """
        return {'status': 'pong'}

class Directories(Resource):
    def get(self):
        """
        Return all directories
        ---
        tags:
            - directories
        responses:
          200:
            description: Directorio
            schema:
              id: User
              properties:
                name:
                  type: string
                  description: The name of the user
                  example: "Rómulo Rodríguez"
                emails:
                  type: array
                  items:
                    type: string
                  description: The email addresses of the user
                  example: ["rjrodrig@ucab.edu.ve", "rjrodriguezr.12@est.ucab.edu.ve"]
        """
        return read_json()

    def post(self):
        """Create a new directory
        ---
        tags:
            - directories
        post:
          summary: Your summary here
          description: Your description here
          parameters:
            - in: body
              name: directory
              schema:
                type: object
                required: true
                properties:
                  name:
                    type: string
                    example: "Rómulo Rodríguez"
                  emails:
                    type: array
                    items:
                      type: string
                    example: ["rjrodrig@ucab.edu.ve", "rjrodriguezr.12@est.ucab.edu.ve"]
          responses:
            '201':
              description: Successful operation

        """
        data = read_json()
        new_id = max([item['id'] for item in data]) + 1 if data else 1
        value = request.get_json()
        value['id'] = new_id
        data.append(value)
        write_json(data)
        return value, 201

class Directory(Resource):
    def get(self, id):
        """Return a directory by ID"""
        data = read_json()
        return next((item for item in data if item['id'] == id), None)

    def put(self, id):
        """Update a directory by ID"""
        data = read_json()
        value = request.get_json()
        value['id'] = id
        data = [item if item['id'] != id else value for item in data]
        write_json(data)
        return value, 201

    def delete(self, id):
        """Delete a directory by ID"""
        data = read_json()
        data = [item for item in data if item['id'] != id]
        write_json(data)
        return '', 204

api.add_resource(Status, '/status')
api.add_resource(Directories, '/directories')
api.add_resource(Directory, '/directories/<int:id>')

@app.route("/swagger")
def swagger_spec():
    swag = swagger(app)
    swag['info']['version'] = "1.0"
    swag['info']['title'] = "My API"
    return jsonify(swag)

SWAGGER_URL = '/swagger-ui'
API_URL = '/swagger'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "My API"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

if __name__ == '__main__':
    app.run(debug=True)
print('tst')