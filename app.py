import psycopg2
from flask import Flask, request, redirect, url_for, flash, session, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from itsdangerous import URLSafeTimedSerializer as Serializer

app = Flask(__name__)
app.secret_key = ''

# Configuración de SendGrid
SENDGRID_API_KEY = '' 

# Serializador para crear y verificar tokens
serializer = Serializer(app.secret_key, salt='password-reset-salt')

def get_db_connection():
    try:
        conn = psycopg2.connect(
            host='',
            user='',
            password='',
            database='',
            port=''
        )
        return conn
    except Exception as ex:
        print("Error de conexión a la base de datos:", ex)
        return None

# Función para enviar correos
def enviar_email(destinatario, asunto, cuerpo):
    mensaje = Mail(
        from_email='gaia.aplication@gmail.com',  # Cambia esto por tu correo en SendGrid
        to_emails=destinatario,
        subject=asunto,
        html_content=cuerpo
    )
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(mensaje)
        print(f"Correo enviado con éxito! Status code: {response.status_code}")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")




@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':

        user = request.form['username']
        password = request.form['password']
        email = request.form['email']

        # Verificar que no haya campos vacíos
        if not user or not email or not password:
            flash("Todos los campos son obligatorios.")
            return redirect(url_for('registro'))


        conn = get_db_connection()
        if conn is None:
            flash("Error de conexión a la base de datos.")
            return redirect(url_for('registro'))

        cursor = conn.cursor()

        # Verificar si el correo ya está registrado
        cursor.execute("SELECT * FROM usuarios WHERE correo = %s", (email,))
        if cursor.fetchone():
            flash("El correo electrónico ya está registrado.")
            cursor.close()
            conn.close()
            return redirect(url_for('registro'))

        # Hashear la contraseña
        hashed_password = generate_password_hash(password)

        # Insertar usuario en la base de datos
        cursor.execute("INSERT INTO usuarios (nombre, correo, contraseña) VALUES (%s, %s, %s)",
                        (user, email, hashed_password))
        conn.commit()

        cursor.close()
        conn.close()

        session['user'] = user
        return redirect(url_for('login'))

    
    return render_template('signUp.html')

@app.route('/')
def home():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    #return redirect(url_for('pagina_principal'))#

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Verificar que no haya campos vacíos
        if not email or not password:
            flash("Todos los campos son obligatorios.")
            return redirect(url_for('login'))

        conn = get_db_connection()
        if conn is None:
            flash("Error de conexión a la base de datos.")
            return render_template('login.html')

        try:
            cursor = conn.cursor()

            # Buscar al usuario en la base de datos
            cursor.execute("SELECT correo, contraseña FROM usuarios WHERE correo = %s", (email,))
            user = cursor.fetchone()  # Devuelve una tupla (correo, contraseña) o None

            if user:
                # Validar la contraseña
                if check_password_hash(user[1], password):  # user[1] es la contraseña
                    session['correo'] = user[0]  # Guarda el correo
                    return redirect(url_for('main'))
                else:
                    flash("Contraseña incorrecta.")
            else:
                flash("El correo electrónico no está registrado.")
        
        except Exception as e:
            flash("Error al iniciar sesión.")
            print(e)

        finally:
            cursor.close()
            conn.close()

    return render_template('login.html')

@app.route('/main')
def main():
    return render_template('main.html')

@app.route('/notas')
def notas():
    return render_template('notas.html')

@app.route('/retos')
def retos():
    return render_template('retos.html')

@app.route('/recuperar_contrasena', methods=['GET', 'POST'])
def recuperar_contrasena():
    if request.method == 'POST':
        email = request.form['email']

        conn = get_db_connection()
        if conn is None:
            flash("Error de conexión a la base de datos.")
            return redirect(url_for('recuperar_contrasena'))

        cursor = conn.cursor()
        cursor.execute("SELECT correo FROM usuarios WHERE correo = %s", (email,))
        usuario = cursor.fetchone()

        if usuario:
            token = serializer.dumps(email, salt='password-reset-salt')
            enlace = url_for('restablecer_contrasena', token=token, _external=True)
            asunto = "Recuperación de contraseña"
            cuerpo = f"""
            <p>Hola, hemos recibido una solicitud para restablecer tu contraseña.</p>
            <p>Si no has solicitado este cambio, ignora este mensaje.</p>
            <p>Para restablecer tu contraseña, haz clic en el siguiente enlace:</p>
            <a href="{enlace}">Restablecer contraseña</a>
            """
            enviar_email(email, asunto, cuerpo)
            flash("Te hemos enviado un correo para recuperar tu contraseña.")
        else:
            flash("El correo electrónico no está registrado.")

        cursor.close()
        conn.close()

    return render_template('recover.html')

@app.route('/restablecer_contrasena/<token>', methods=['GET', 'POST'])
def restablecer_contrasena(token):
    try:
        email = serializer.loads(token, salt='password-reset-salt', max_age=900)
    except:
        flash("El enlace de restablecimiento ha caducado o es inválido.", "error")
        return redirect(url_for('recuperar_contrasena'))

    if request.method == 'POST':
        nueva_contrasena = request.form['nueva_contrasena']
        hashed_password = generate_password_hash(nueva_contrasena)

        conn = get_db_connection()
        if conn is None:
            flash("Error de conexión a la base de datos.")
            return redirect(url_for('recuperar_contrasena'))

        cursor = conn.cursor()
        cursor.execute("UPDATE usuarios SET contraseña = %s WHERE correo = %s", (hashed_password, email))
        conn.commit()

        cursor.close()
        conn.close()

        flash("Tu contraseña ha sido restablecida con éxito.", "success")
        return redirect(url_for('login'))

    return render_template('reset.html')

if __name__ == '__main__':
    app.run(debug=True)
