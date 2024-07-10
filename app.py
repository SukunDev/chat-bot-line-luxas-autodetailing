from flask import Flask, send_from_directory
from models import db
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

@app.route('/assets/<path:filename>')
def assets(filename):
    return send_from_directory('assets', filename)