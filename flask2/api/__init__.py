from flask import render_template, request, Flask
from config import Config
from api.database import DatabaseConnection

def init_app():
    """Crea y configura la aplicación Flask"""
    
    app = Flask(__name__, static_folder = Config.STATIC_FOLDER, template_folder = Config.TEMPLATE_FOLDER)
    
    app.config.from_object(Config)
    
    @app.route('/actors/<int:actor_id>', methods = ['GET'])
    def get_actor(actor_id):
        sql = "SELECT actor_id, first_name, last_name, last_update FROM sakila.actor WHERE actor_id = %s;"
        params = actor_id,
        result = DatabaseConnection.fetch_one(sql, params)
        if result is not None:
            return {
            "id": result[0],
            "nombre": result[1],
            "apellido": result[2],
            "ultima_actualizacion": result[3]
            }, 200
        return {"msg": "No se encontró el actor"}, 404
    
    @app.route('/updactors/<int:actor_id>', methods = ['PUT'])
    def update_actor(actor_id):
        sql = "UPDATE sakila.actor SET last_update = %s WHERE actor.actor_id = %s;"
        params = request.args.get('last_update', ''), actor_id
        DatabaseConnection.execute_query(sql, params)
        return {"msg": "Datos del actor actualizados con éxito"}, 200

    return app