import os
from flask import Flask
from api.resume import resume_route
from api.position import position_route
from api.similarity import similarity_route
from mongoengine import connect

app = Flask(__name__)
app.register_blueprint(resume_route)
app.register_blueprint(position_route)
app.register_blueprint(similarity_route)

connect(host=os.environ.get('MONGO_URI'))

if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0", port=int("5000"), debug=True)
