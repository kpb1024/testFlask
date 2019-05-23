from flask import current_app, g
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

def init_app(app):
    app.teardown_appcontext(close_db)
