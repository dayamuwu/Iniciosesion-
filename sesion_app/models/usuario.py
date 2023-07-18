from sesion_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX=re.compile(r"^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$")

class Usuario:
    def __init__(self,data):
        self.id=data['id']
        self.nombre=data['nombre']
        self.apellido=data['apellido']
        self.correo=data['correo']
        self.contrasena=data['contrasena']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']


    @classmethod
    def get_usuario(cls,data):
        query="SELECT * FROM usuarios WHERE id=%(id)s;"
        result=connectToMySQL("sesion_db").query_db(query,data)
        return cls(result[0]) 


    @classmethod
    def guardar(cls,data):
        query = "INSERT INTO usuarios (nombre,apellido,correo,contrasena) VALUES (%(nombre)s,%(apellido)s,%(correo)s,%(contrasena)s);"
        return connectToMySQL("sesion_db").query_db(query, data)


    @classmethod
    def get_by_correo(cls,data):
        query = "SELECT * FROM usuarios WHERE correo = %(correo)s;"
        result = connectToMySQL("sesion_db").query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])


    @classmethod
    def get_all(cls):
        query="SELECT * FROM usuarios;"
        result=connectToMySQL("sesion_db").query_db(query)
        all_usu=[]
        for usu in result:
            all_usu.append(cls(usu))
        return all_usu


    @staticmethod
    def validar_usuario(registro):
        email={
            "correo":registro['correo']
        }
        is_valid = True 
        if len(registro['nombre']) < 3:
            flash("Nombre debe contener al menos 3 caracteres")
            is_valid = False
        if len(registro['apellido']) < 3:
            flash("Apellido debe contener al menos 3 caracteres")
            is_valid = False
        if len(registro['contrasena']) < 8:
            flash("Contraseña debe tener al menos 8 caracteres")
            is_valid = False
        if not EMAIL_REGEX.match(email['correo']):
            flash("Correo no valido")
            is_valid = False
        elif Usuario.get_by_correo(email):
            flash("Correo ya existe")
            is_valid = False
        if registro['contrasena']!= registro['confcontrasena']:
            flash('Contraseñas no coinciden')
            is_valid = False
        espacio=False
        mayus=False
        minus=False
        numeros=False
        for contr in registro['contrasena']:
            if contr.isspace()==True:
                espacio=True
            if contr.isdigit()==True:
                numeros=True
            if contr.islower()== True:
                minus=True
            if contr.isupper()== True:
                mayus=True
        if espacio==True:
            flash("Contraseña no debe tener espacios en blanco")
            is_valid = False
        if mayus==False:
            flash("Contraseña deben contener al menos una mayuscula")
            is_valid = False
        if numeros==False:
            flash("Contraseña deben contener al menos un numero")
            is_valid = False
        if minus==False:
            flash("Contraseña deben contener al menos una minuscula")
            is_valid = False
        return is_valid
