import os
from flask import Flask
from api.resume import resume_route
from mongoengine import connect

app = Flask(__name__)
app.register_blueprint(resume_route)

connect(host=os.environ.get('MONGO_URI'))

if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0", port=int("3000"), debug=True)
