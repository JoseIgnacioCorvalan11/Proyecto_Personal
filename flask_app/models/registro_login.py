import datetime
from flask_app import app     
import re
from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
DIGITO_REGEX = re.compile(r'\d+')
MAYUSCULA_REGEX = re.compile(r'[A-Z]+')

class Proyecto:
    def __init__(self, data ):
        self.id = data['id']
        self.name = data['name']
        self.last_name = data['last_name']
        self.mail = data['mail']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @staticmethod
    def validar_registro(formulario):
        fecha_actual = datetime.datetime.now()

        valido = True
        if not EMAIL_REGEX.match(formulario['mail']):
            flash("Email no valido! ERROR ERROR!!!")
            valido = False
        if len(formulario['name']) < 3:
            flash("Nombre debe ser al menos 3 caracteres largos")
            valido = False
        if len(formulario['last_name']) < 3:
            flash("Nombre debe ser al menos 3 caracteres largos")
            valido = False
        if not DIGITO_REGEX.search(formulario['password']):
            flash("Se necesita al menos 1 digito")
            valido = False
        if not MAYUSCULA_REGEX.search(formulario['password']):
            flash("Se necesita al menos 1 Mayuscula")
            print(formulario['password'])
            valido = False
        # if int(formulario['radio']) == 1:
        #     valido = True
        if len(formulario['date']) < 1:
            print(fecha_actual, "FECHA ACTUAL"*10)
            flash("Por favor llene su cumple")
            valido = False
        if len(formulario['date']) > 1:
            fecha_formulario = datetime.datetime.strptime(formulario["date"], "%Y-%m-%d")
            total_fecha =  fecha_actual - fecha_formulario
            convertirfechaenINT = int(total_fecha.days)
            print(convertirfechaenINT, "TOTAL RESTAR FECHAS"*10)
            if convertirfechaenINT < 6570:
                flash("Usuario debe ser mayor de 18")
                valido = False
        return valido

    @classmethod
    def save(cls, data):
        query="INSERT INTO registro_login (name , last_name, mail, password) VALUES ( %(name)s , %(last_name)s , %(mail)s , %(password)s );"
        return connectToMySQL('schema_musica').query_db( query, data )

    @classmethod
    def get_all(cls, id):
        query= "SELECT * FROM registro_login WHERE id != %(id)s;"
        results = connectToMySQL('schema_musica').query_db(query, id)
        print("QUE HAY AQUI?", results)
        proyecto_result = []
        for proyecto in results:
            proyecto_result.append( cls(proyecto) )
        return proyecto_result

    @classmethod
    def getEmail(cls, data):
        print(data, "Esto esta en el data")
        query = "SELECT * FROM registro_login WHERE mail = %(mail)s;"
        results = connectToMySQL('schema_musica').query_db( query, data )
        if len(results) < 1:
            return False
        print("RETORNO GET EMAIL:",results)
        return cls(results[0])

    @classmethod
    def delete(cls, data):
        query= "DELETE FROM registro_login WHERE id = %(id)s;"
        return connectToMySQL('schema_musica').query_db( query, data )

    @classmethod
    def get_one(cls, data):
        query= "SELECT * FROM registro_login WHERE id = %(id)s;"
        results = connectToMySQL('schema_musica').query_db(query, data)
        print("QUE HAY AQUI?", results)
        if len(results) < 1:
            return False
        print("RETORNO GET EMAIL:",results)
        return cls(results[0])