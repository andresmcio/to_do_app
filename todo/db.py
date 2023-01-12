import mysql.connector
import click #Ejecuta comandos en terminal para interactuar con mysql
from flask import current_app, g # Current mantiene ejecución de app en curso, g asigna valores de variables entorno 
from flask.cli import with_appcontext # Trae contexto de aplicación como dirección de host
from .schema import instructions # Usa scripts de interacciones con mysql

def get_db():
    if 'db' not in g:
        g.db = mysql.connector.connect(
            host = current_app.config['DATABASE_HOST'],
            user = current_app.config['DATABASE_USER'],
            password = current_app.config['DATABASE_PASSWORD'],
            database = current_app.config['DATABASE']
        )
        g.c = g.db.cursor(dictionary = True)
    return g.db, g.c

def close_db(e = None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db, c = get_db()

    for i in instructions:
        c.execute(i)

    db.commit()


@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Starting database')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)