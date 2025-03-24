from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash  # type: ignore
from flask_sqlalchemy import SQLAlchemy  # type: ignore
import mariadb  # type: ignore
import hashlib

app = Flask(__name__)
app.secret_key = "1234"

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, descripcion, precio, categoria, imagen, stock FROM productos")
    productos = cursor.fetchall()
    conn.close()

    productos_json = [
        {"id": p[0], "nombre": p[1], "descripcion": p[2], "precio": p[3], "categoria": p[4], "imagen": p[5], "stock": p[6]}
        for p in productos
    ]

    return render_template('index.html', productos=productos_json)

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        correo_electronico = request.form['correo']
        hashed_password = request.form['contraseña']

        # Hashear la contraseña antes de almacenarla
        #hashed_password = hashlib.sha256(hashed_password.encode()).hexdigest()

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("INSERT INTO usuarios (nombre, apellido, correo_electronico, hashed_password) VALUES (?, ?, ?, ?)", 
                           (nombre, apellido, correo_electronico, hashed_password))
            conn.commit()
        except mariadb.IntegrityError:
            return "Error: El correo ya está registrado."
        finally:
            conn.close()

        return redirect(url_for('index'))

    return render_template('registro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form['correo']
        contraseña = request.form['contraseña']

        conn = get_db_connection()
        cursor = conn.cursor()

        # Obtener la contraseña almacenada de la base de datos
        cursor.execute("SELECT id, nombre, hashed_password FROM usuarios WHERE correo_electronico = ?", (correo,))
        user = cursor.fetchone()
        conn.close()

        if user:
            usuario_id, usuario_nombre, hashed_password = user
            # Comparar la contraseña ingresada con la almacenada
            if contraseña == hashed_password:
                session['user_id'] = usuario_id  # Guardar usuario en sesión
                session['user_name'] = usuario_nombre  # Guardar nombre en sesión
                flash("Inicio de sesión exitoso", "success")  # Mensaje de éxito
                return redirect(url_for('index'))
            else:
                flash("Error: Contraseña incorrecta", "danger")  
        else:
            flash("Error: Usuario no encontrado", "danger")

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)  # Eliminar usuario de la sesión
    flash("Has cerrado sesión exitosamente", "info")  # Mensaje de confirmación
    return redirect(request.referrer or url_for('login'))  # Redirigir a la página anterior o a login si no hay referencia

@app.route('/about')
def about():
    return render_template('about.html')

#Conexion a MariaDB sin ORM
def get_db_connection():
    return mariadb.connect(
        user="railway",
        password="Amdwzi-JlqxbQAzQFP~i-zZWK5L1J0P8",
        host="switchyard.proxy.rlwy.net",
        port=35476,
        database="railway"
    )

if __name__ == "__main__":
    app.run(debug=True)