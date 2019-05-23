from flask import current_app, g
from flask.cli import with_appcontext
from ssms.mysql import MySQL

def get_db():
    if 'mysql_db' not in g:
	g.mysql_db = MySQL(current_app)
    return g.mysql_db.get_db() 

def get_results(cursor):
    return list(dict((cursor.description[idx][0], value) for idx, value in enumerate(row)) for row in cursor._rows)

def close_db(e=None):
    db = g.pop('mysql_db', None)
    if db is not None:
        db.teardown_request(None)


#def init_db():
#    """Clear existing data and create new tables."""
#    db = get_db()
#    with current_app.open_resource('schema.sql') as f:
#        db.executescript(f.read().decode('utf8'))


#@click.command('init-db')
#@with_appcontext
#def init_db_command():
#    """Clear existing data and create new tables."""
#    init_db()
#    click.echo('Initialized the database.')


def init_app(app):
    """Register database functions with the Flask app. This is called by
    the application factory.
    """
    app.teardown_appcontext(close_db)
    #app.cli.add_command(init_db_command)
