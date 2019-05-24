import os
from flask import Flask

def create_app(test_config=None):

    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        #DATABASE=os.path.join(app.instance_path, 'ssms.sqlite') 
	#os.makedirs(app.instance_path)
	MYSQL_DATABASE_USER='root',
	MYSQL_DATABASE_PASSWORD='13148899',
	MYSQL_DATABASE_DB='ssms'
    )

    from ssms import db
    db.init_app(app)

    from ssms import auth, info
    app.register_blueprint(auth.bp)
    app.register_blueprint(info.bp)
    app.add_url_rule('/', endpoint='index')

    return app
