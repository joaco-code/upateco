import csv
from flask import render_template, request, Flask
from config import Config
from database import DatabaseConnection

def init_app():
    """Crea y configura la aplicación Flask"""
    
    app = Flask(__name__, static_folder = Config.STATIC_FOLDER, template_folder = Config.TEMPLATE_FOLDER)
    
    app.config.from_object(Config)

    @app.route('/')
    def hello_world():
        return 'Hola Mundo!'

    # @app.route('/login', methods=['GET', 'POST'])
    # def login():
    #     if request.method == 'POST':
    #         return logearse()
    #     else:
    #         return mostrar_formulario()

    @app.post('/login')
    def login_post():
        return logearse()
    
    @app.get('/login')
    def login_get():
        return mostrar_formulario()
    
    
    @app.route('/perfil/<string:username>')
    def perfil(username):
        return f'Bienvenido {username}!'
    

    def obtener_usuarios():
        usuarios = {}
        with open('usuarios.csv', 'r') as f:
            reader = csv.reader(f)
            next(reader)  # Saltamos la primera fila (cabecera)
            for row in reader:
                usuarios[row[0]] = row[1]
        
        return usuarios
    

    def logearse():
        usuarios = obtener_usuarios()
        nombre = request.form['nombre']
        contrasena = request.form['contrasena']
        if usuarios.get(nombre) == contrasena:
            return f"Inicio de sesión exitoso, Bienvenid@ <b>{nombre.upper()}</b>"
        else:
            return "Error: Nombre de usuario o contraseña incorrectos"

    def mostrar_formulario():
        return render_template('formulario_login.html')  # Asumiendo que tienes una plantilla llamada 'formulario_login.html'
    
   
    # @app.route('/users')
    # def get_users():
    #     register_date = request.args.get('register_date','')
    #     if register_date != '':
    #         return get_recents_users(filter = register_date)
    #     else:
    #         return get_recents_users()


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
    
    
    @app.route('/actors', methods = ['GET'])
    def get_actors():
        sql = "SELECT actor_id, first_name, last_name, last_update FROM sakila.actor;"
        results = DatabaseConnection.fetch_all(sql)
        actors = []
        for result in results:
            actors.append({
                "id": result[0],
                "nombre": result[1],
                "apellido": result[2],
                "ultima_actualizacion": result[3]
                })
        return actors, 200
    
    
    @app.route('/del/<int:actor_id>', methods = ['DELETE'])
    def delete_actor(actor_id):
        sql = "DELETE FROM sakila.actor WHERE actor.actor_id = %s;"
        params = actor_id,
        DatabaseConnection.execute_query(sql, params)
        
        return {"msg": "Actor eliminado con éxito"}, 204


    
    return app