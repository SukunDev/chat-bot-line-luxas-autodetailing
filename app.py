from flask import Flask
from models import db, LineUser, Keyword
from flask_migrate import Migrate


from routes.home_bp import home_bp
from routes.webhook_bp import webhook_bp
from routes.api_bp import api_bp

app = Flask(__name__)
app.config.from_object('config')

db.init_app(app)

migrate = Migrate(app, db)

app.register_blueprint(home_bp, url_prefix='/')
app.register_blueprint(webhook_bp, url_prefix='/webhook')
app.register_blueprint(api_bp, url_prefix='/api')
