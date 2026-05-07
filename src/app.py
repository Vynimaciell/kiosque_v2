import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from flask import Flask
from models import init_db
from routes import bp

BASE     = os.path.dirname(__file__)
FRONTEND = os.path.join(BASE, '..', 'frontend')

app = Flask(
    __name__,
    template_folder=os.path.join(FRONTEND, 'pages'),
    static_folder=os.path.join(FRONTEND),
    static_url_path=''
)

app.secret_key = os.environ.get('SECRET_KEY', 'kiosque_rental_dev')

app.register_blueprint(bp)

with app.app_context():
    init_db()

if __name__ == '__main__':
    app.run(debug=False, port=5000)
