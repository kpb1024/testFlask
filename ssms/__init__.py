import os

from flask import Flask
<<<<<<< HEAD
from flask_sqlalchemy import SQLAlchemy
=======
from flask_jsglue import JSGlue
>>>>>>> 266f41eeae4d225dbf423f5cf25d955d8177b373

def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
<<<<<<< HEAD
=======
    jsglue = JSGlue()
    jsglue.init_app(app)  # 让js文件中可以使用url_for方法
>>>>>>> 266f41eeae4d225dbf423f5cf25d955d8177b373
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY='dev',
        # store the database in the instance folder
        DATABASE=os.path.join(app.instance_path, 'ssms.sqlite'),
<<<<<<< HEAD
	SQLALCHEMY_DATABASE_URI='sqlite:////ssms.db',
    )
    orm = SQLAlchemy(app)
=======
    )
>>>>>>> 266f41eeae4d225dbf423f5cf25d955d8177b373

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # register the database commands
    from ssms import db
    db.init_app(app)

    # apply the blueprints to the app
    from ssms import auth, info
    app.register_blueprint(auth.bp)
    app.register_blueprint(info.bp)

    # make url_for('index') == url_for('blog.index')
    # in another app, you might define a separate main index here with
    # app.route, while giving the blog blueprint a url_prefix, but for
    # the tutorial the blog will be the main index
    app.add_url_rule('/', endpoint='index')

    return app
