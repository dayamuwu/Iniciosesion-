from sesion_app import app
from flask import render_template, request, redirect, session
from sesion_app.models.usuario import Usuario
from flask_bcrypt import Bcrypt
from flask import flash
bcrypt = Bcrypt(app)
app.secret_key = 'ch3st3r@%!gn'


@app.route('/')
def index():
    return render_template("index.html")



@app.route('/nuevo', methods=['POST'])
def registro():
    pw_hash = bcrypt.generate_password_hash(request.form['contrasena'])
    data = {
        "nombre": request.form['nombre'],
        "apellido": request.form['apellido'],
        "correo": request.form['correo'],
        "contrasena" : pw_hash
    }
    if not Usuario.validar_usuario(request.form):
        return redirect("/")
    usuario_id = Usuario.guardar(data)
    session['usuario_id'] = usuario_id
    return redirect(f"/veamos/{session['usuario_id']}")


@app.route('/veamos/<int:id>')
def ver(id):
    if "usuario_id" not in session:
        return redirect("/")
    data={
        "id":id
    }
    Usuario.get_usuario(data)
    un_usuario=Usuario.get_usuario(data)
    todos_usuarios=Usuario.get_all()
    return render_template("veamos.html",todos_usuarios=todos_usuarios,un_usuario=un_usuario)


@app.route('/login', methods=['POST'])
def login():
    data = {
        "correo" : request.form["correo"]
    }
    usuario_in_db = Usuario.get_by_correo(data)
    if not usuario_in_db:
        flash("Correo/Contraseña erroneos")
        return redirect("/")
    if not bcrypt.check_password_hash(usuario_in_db.contrasena, request.form['contrasena']):
        flash("Correo/Contraseña erroneos")
        return redirect('/')
    session['usuario_id'] = usuario_in_db.id
    return redirect(f"/veamos/{session['usuario_id']}")


@app.route('/quitarsesion')
def quitar():
    session.clear()
    return redirect('/')