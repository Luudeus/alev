from flask_mysqldb import MySQL
import os
from user_validation.user_data_format import *
from user_validation.user_login_validator import *
from user_validation.user_register_validator import *
from user_validation.rut_format import rut_format
from dotenv import load_dotenv
from flask import (
    Flask,
    render_template,
    flash,
    redirect,
    jsonify,
    url_for,
    request,
    session,
)
from flask_session import Session
from pagination import Pagination
from functions import login_required, logged_in_redirect, admin_required
from werkzeug.security import check_password_hash, generate_password_hash

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Load environment variables from .env
load_dotenv()

# Configure Flask-MySQLdb
app.config["MYSQL_HOST"] = os.getenv("DB_HOST")
app.config["MYSQL_USER"] = os.getenv("DB_USER")
app.config["MYSQL_PASSWORD"] = os.getenv("DB_PASS")
app.config["MYSQL_DB"] = os.getenv("DB_NAME")
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

# Initialize MySQL
mysql = MySQL(app)


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


def database_user_register(cursor, rut, name, mail, phone, address, password, permission="normal"):
    """
    Register a user into the database.

    This function registers a user into the database by inserting their RUT, name, email,
    phone, permission level, and password into the appropriate database table. It uses the
    provided cursor to execute the SQL query for registration.

    Args:
        cursor: A database cursor object for executing SQL queries.
        rut (str): The user's RUT (Rol Único Tributario), a unique identification number.
        name (str): The user's name.
        mail (str): The user's email address.
        phone (str): The user's phone number.
        password (str): The user's password.
        permission (str, optional): The user's permission level (e.g., "normal" or "admin").
                                    Defaults to "normal" if not specified.

    Returns:
        None
    """

    cursor.execute(
        "INSERT INTO User (RUT, nombre, correo, telefono, direccion, permisos, contrasenia) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (
            rut,
            name,
            mail,
            phone,
            address,
            permission,
            password,
        ),
    )
    mysql.connection.commit()


def search_users(template_name):
    # Retrieve query parameters for search, ordering, and pagination
    search_term = request.args.get("search", default="")
    order = request.args.get("o", default="id_book")
    direction = request.args.get("d", default="ASC").upper()
    page = request.args.get("page", 1, type=int)
    per_page = 10  # Limit of items per page

    # Connect to the database
    cursor = mysql.connection.cursor()

    # Start building the SQL query
    base_query = "SELECT * FROM User"
    where_clause = ""
    order_clause = ""

    # Add a WHERE clause if a search term is provided
    if search_term:
        where_clause = " WHERE nombre LIKE %s"

    # Validate ordering parameters and add ORDER BY clause
    valid_columns = ["rut", "nombre", "correo", "telefono", "direccion", "permisos"]
    if order in valid_columns and direction in ["ASC", "DESC"]:
        order_clause = f" ORDER BY {order} {direction}"

    # Pagination clause
    pagination_clause = f" LIMIT {per_page} OFFSET {(page - 1) * per_page}"

    # Complete SQL query for users
    query = f"{base_query}{where_clause}{order_clause}{pagination_clause}"

    # Execute the query with parameters if needed
    try:
        if search_term:
            cursor.execute(query, (f"%{search_term}%",))
        else:
            cursor.execute(query)
    except Exception as e:
        print("Error during query execution:", e)

    # Fetch the results
    users = cursor.fetchall()

    # Query for total count of users (for pagination)
    count_query = "SELECT COUNT(*) FROM User" + where_clause
    cursor.execute(count_query, (f"%{search_term}%",) if search_term else ())
    result = cursor.fetchone()
    total_users = result["COUNT(*)"] if result else 0

    # Calculate total pages
    total_pages = (total_users + per_page - 1) // per_page

    cursor.close()

    # Check if the request is an AJAX request
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return jsonify(
            {"users": users, "total_pages": total_pages, "current_page": page}
        )

    # Create a Pagination object
    pagination = Pagination(page=page, per_page=per_page, total_count=total_users)

    # Render the template with the fetched users and pagination data
    return render_template(f"{template_name}.html", users=users, pagination=pagination)

# Route functions
@app.route("/")
@login_required
def index():
    """Show Junta de Vecinos's homepage"""
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
@logged_in_redirect
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    if request.method == "GET":
        # User reached route via GET (as by clicking a link or via redirect)
        return render_template("login.html")

    # User reached route via POST (as by submitting a form via POST)
    else:
        # Get form data
        rut = request.form.get("rut")
        password = request.form.get("password")

        # Ensure both RUT and password were submitted
        errors = validate_login_input(rut, password)
        if errors:
            for error in errors:
                flash(error, "warning")
            return render_template("login.html")

        # Format RUT to delete spaces and hyphens
        rut = format_rut(request.form.get("rut"))

        # Create a new database cursor
        cursor = mysql.connection.cursor()

        # Query database for rut
        cursor.execute("SELECT * FROM User WHERE RUT = %s", (rut,))
        rows = cursor.fetchall()

        # Ensure rut exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["contrasenia"], request.form.get("password")
        ):
            flash("RUT y/o contraseña inválidos", "warning")
            return render_template("login.html")

        # Remember which user has logged in
        session["user_id"] = rows[0]["RUT"]
        
        # Remember name of the user
        session["username"] = rows[0]["nombre"]

        # Remember permission type of the user
        session["permission_type"] = rows[0]["permisos"]

        # Close the db cursor
        cursor.close()

        # Redirect user to home page
        return redirect("/")


@app.route("/register", methods=["GET", "POST"])
@logged_in_redirect
def register():
    """Register user"""
    if request.method == "GET":
        # User reached route via GET (as by clicking a link or via redirect)
        return render_template("register.html")
    else:
        # Get form data
        rut = request.form.get("rut")
        name = request.form.get("name")
        mail = request.form.get("email")
        phone = format_phone(request.form.get("phone"))
        address = request.form.get("address")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Validate user's entries
        errors = validate_register_input(rut, name, mail, phone, address, password, confirmation)
        if errors:
            for error in errors:
                flash(error, "warning")
            return render_template("register.html")

        # Format RUT, mail, name, and phone
        formatted_rut, formatted_mail, formatted_name, formatted_phone = format_data(rut, mail, name, phone)

        # Check if rut is available
        cursor = mysql.connection.cursor()

        # Insert the user into the database
        try:
            cursor.execute("SELECT * FROM User WHERE RUT = %s", (formatted_rut,))
            rows = cursor.fetchall()
            if len(rows) > 0:
                flash("Error al registrarse: el usuario ya existe", "warning")
                return render_template("register.html")
        finally:
            cursor.close()

        # Insert the user into the users table
        try:
            cursor = mysql.connection.cursor()
            database_user_register(
                cursor,
                formatted_rut,
                formatted_name,
                formatted_mail,
                formatted_phone,
                address,
                hash_password(password),
            )
        except Exception as e:
            # Handle the exception
            print("Error al intentar registrar el usuario:", e)
            flash("Error al registrar el usuario", "warning")
            return render_template("register.html")
        finally:
            cursor.close()

        flash("Usuario creado correctamente", "success")
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id and permissions
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/lista-de-usuarios", methods=["GET"])
def lista_de_usuarios():
    return search_users("lista-de-usuarios")


@app.route("/agregar-usuarios", methods=["GET", "POST"])
@admin_required
def agregar_usuarios():
    if request.method == "GET":
        # User reached route via GET (as by clicking a link or via redirect)
        return render_template("agregar-usuarios.html")
    else:
        # Get form data
        rut = request.form.get("rut")
        name = request.form.get("name")
        mail = request.form.get("email")
        phone = format_phone(request.form.get("phone"))
        address = request.form.get("address")
        permission = request.form.get("permisos")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Validate user's entries
        errors = validate_register_input(
            rut, name, mail, phone, address, password, confirmation, permission
        )
        if errors:
            for error in errors:
                flash(error, "warning")
            return render_template("agregar-usuarios.html")

        # Format RUT, mail, name, and phone
        formatted_rut, formatted_mail, formatted_name, formatted_phone = format_data(
            rut, mail, name, phone
        )

        # Check if rut is available
        cursor = mysql.connection.cursor()

        # Insert the user into the database
        try:
            cursor.execute("SELECT * FROM User WHERE RUT = %s", (formatted_rut,))
            rows = cursor.fetchall()
            if len(rows) > 0:
                flash("Error al registrar: el usuario ya existe", "warning")
                return render_template("agregar-usuarios.html")
        finally:
            cursor.close()

        # Insert the user into the users table
        try:
            cursor = mysql.connection.cursor()
            database_user_register(
                cursor,
                formatted_rut,
                formatted_name,
                formatted_mail,
                formatted_phone,
                address,
                hash_password(password),
                permission,
            )
            mysql.connection.commit()
        except Exception as e:
            # Handle the exception
            print("Error al intentar registrar el usuario:", e)
            flash("Error al registrar el usuario", "warning")
            return render_template("agregar-usuarios.html")
        finally:
            cursor.close()

        flash(
            f"Usuario creado correctamente.\nRUT: {rut}\nNombre: {name}\nCorreo: {mail}\nTeléfono: {phone}\nDirección: {address}\nPermisos: {permission}\nContraseña: {password}",
            "success",
        )
        return render_template("agregar-usuarios.html")


@app.route("/editar-usuarios", methods=["GET"])
@admin_required
def editar_usuarios():
    # Retrieve query parameters for search, ordering, and pagination
    search_term = request.args.get("search", default="")
    order = request.args.get("o", default="nombre")
    direction = request.args.get("d", default="ASC").upper()
    page = request.args.get("page", 1, type=int)
    per_page = 10  # Limit of items per page

    # Connect to the database
    cursor = mysql.connection.cursor()

    # Start building the SQL query
    base_query = "SELECT RUT, nombre, correo, telefono, direccion, permisos FROM User"
    where_clause = ""
    order_clause = ""

    # Add a WHERE clause if a search term is provided
    if search_term:
        where_clause = " WHERE RUT LIKE %s OR nombre LIKE %s OR correo LIKE %s OR telefono LIKE %s OR direccion LIKE %s or PERMISOS LIKE %s"

    # Validate ordering parameters and add ORDER BY clause
    valid_columns = ["rut", "nombre", "correo", "telefono", "direccion", "permisos"]
    if order in valid_columns and direction in ["ASC", "DESC"]:
        order_clause = f" ORDER BY {order} {direction}"

    # Pagination clause
    pagination_clause = f" LIMIT {per_page} OFFSET {(page - 1) * per_page}"

    # Complete SQL query for users
    query = f"{base_query}{where_clause}{order_clause}{pagination_clause}"

    # Execute the query with parameters if needed
    try:
        if search_term:
            cursor.execute(query, (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%", f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"))
        else:
            cursor.execute(query)
    except Exception as e:
        print("Error during query execution:", e)

    # Fetch the results
    users = cursor.fetchall()

    # Query for total count of users (for pagination)
    count_query = "SELECT COUNT(*) FROM User" + where_clause
    params = (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%", f"%{search_term}%", f"%{search_term}%", f"%{search_term}%") if search_term else ()
    cursor.execute(count_query, params)
    result = cursor.fetchone()
    total_users = result["COUNT(*)"] if result else 0

    # Calculate total pages
    total_pages = (total_users + per_page - 1) // per_page

    cursor.close()

    # Check if the request is an AJAX request
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return jsonify(
            {"users": users, "total_pages": total_pages, "current_page": page}
        )

    # Create a Pagination object
    pagination = Pagination(page=page, per_page=per_page, total_count=total_users)

    # Render the template with fetched users and pagination data
    return render_template("editar-usuarios.html", users=users, pagination=pagination)


@app.route("/edit-user", methods=["GET", "POST"])
@admin_required
def edit_user():
    if request.method == "GET":
        # Get the RUT from the query parameter
        user_rut = request.args.get("id")
        if not user_rut:
            flash("No se proporcionó el RUT", "warning")
            return redirect(url_for("editar_usuarios"))

        # Connect to the database
        cursor = mysql.connection.cursor()

        # Retrieve the user's data
        try:
            cursor.execute("SELECT RUT, nombre, correo, telefono, direccion, permisos FROM User WHERE RUT = %s", (user_rut,))
            user = cursor.fetchone()
        except Exception as e:
            print("No se pudieron obtener los datos del usuario:", e)
            flash("No se pudieron obtener los datos del usuario", "warning")
            return redirect(url_for("editar_usuarios"))

        cursor.close()

        # Check if the user exists
        if not user:
            flash("Usuario no encontrado", "warning")
            return redirect(url_for("editar_usuarios"))

        # Render the edit-user.html template passing the user's data
        return render_template("edit-user.html", user=user)
    else:
        # POST request logic for updating user details
        try:
            # Retrieve the RUT and form data
            formatted_rut = request.form.get("hidden_formatted_rut")
            user_rut = request.form.get("rut")
            nombre = request.form.get("nombre")
            correo = request.form.get("correo")
            telefono = request.form.get("telefono")
            direccion = request.form.get("direccion")
            permisos = request.form.get("permisos")
            
            # Format phone number
            formatted_telefono = format_phone(telefono)
            
            # Check phone's number length
            if not is_phone_valid(formatted_telefono):
                flash("El teléfono debe contener 11 dígitos", "warning")
                raise Exception("El teléfono debe contener 11 dígitos.")

            # Check if mail's format is correct
            if not is_email_complex(correo):
                flash("El correo debe estar en un formato correcto. Ejemplo: 'example@example.com'", "warning")
                raise Exception("El correo no tiene un formato adecuado.")
            
            # Check if the user exists
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT RUT FROM User WHERE RUT = %s", (user_rut,))
            if cursor.fetchone() is None:
                cursor.close()
                flash("Usuario no encontrado", "warning")
                return redirect(url_for("editar_usuarios"))

            # Update the user's data
            update_query = """
                UPDATE User
                SET nombre = %s, correo = %s, telefono = %s, direccion = %s, permisos = %s
                WHERE RUT = %s
            """
            cursor.execute(update_query, (nombre, correo, formatted_telefono, direccion, permisos, user_rut))
            mysql.connection.commit()
            cursor.close()
            flash(f"Los datos del usuario RUT: {formatted_rut} han sido actualizados", "success")
            return redirect(url_for("editar_usuarios"))

        except Exception as e1:
            print("Error al actualizar el usuario:", e1)
            
            # Connect to the database
            cursor = mysql.connection.cursor()

            # Retrieve the user's data
            try:
                cursor.execute("SELECT RUT, nombre, correo, telefono, direccion, permisos FROM User WHERE RUT = %s", (user_rut,))
                user = cursor.fetchone()
            except Exception as e2:
                print("No se pudieron obtener los datos del usuario:", e2)
                return redirect(url_for("editar_usuarios"))

            cursor.close()
            flash("Error al actualizar el usuario", "warning")
            return render_template("edit-user.html", user=user)


@app.route("/delete-user", methods=["GET"])
@admin_required
def delete_user():
    # Get the RUT from the query parameter
    user_rut = request.args.get("id")
    if not user_rut:
        flash("No se proporcionó el RUT", "warning")
        return redirect(url_for("editar_usuarios"))
    
    # Connect to the database
    cursor = mysql.connection.cursor()

    # Delete the user by RUT
    try:
        cursor.execute("DELETE FROM User WHERE RUT = %s", (user_rut,))
        mysql.connection.commit()
    except Exception as e:
        print("No se pudo eliminar el usuario:", e)
        flash("No se pudo eliminar el usuario", "warning")
        return render_template("editar-usuarios.html")
    cursor.close()
    
    flash(f"Se eliminó el usuario RUT: {rut_format(user_rut)}", "success")
    return redirect(url_for("editar_usuarios"))


@app.route("/mi-cuenta", methods=["GET", "POST"])
@login_required
def mi_cuenta():
    if request.method == "GET":
        # Retrieve RUT from user's session
        user_rut = session.get("user_id")
        if not user_rut:
            flash("No se proporcionó el RUT del usuario", "warning")
            return redirect(url_for("index"))

        # Connect to the database
        cursor = mysql.connection.cursor()

        # Retrieve the user's data
        try:
            cursor.execute("SELECT * FROM User WHERE RUT = %s", (user_rut,))
            user = cursor.fetchone()
        except Exception as e:
            print("No se pudieron obtener los datos del usuario:", e)
            flash("No se pudieron obtener los datos del usuario", "warning")
            return redirect(url_for("index"))

        cursor.close()

        # Check if the user exists
        if not user:
            flash("Usuario no encontrado", "warning")
            return redirect(url_for("index"))

        # Render the mi-cuenta.html template passing the user's data
        return render_template("mi-cuenta.html", user=user)
    
    elif request.method == "POST":
        try:
            # Retrieve the RUT and form data
            user_rut = session.get("user_id")
            nombre = request.form.get("nombre")
            correo = request.form.get("correo")
            telefono = request.form.get("telefono")
            direccion = request.form.get("direccion")

            # Connect to the database
            cursor = mysql.connection.cursor()
            
            # Format phone number
            formatted_telefono = format_phone(telefono)
            
            # Check phone's number length
            if not is_phone_valid(formatted_telefono):
                flash("El teléfono debe contener 11 dígitos", "warning")
                raise Exception("El teléfono debe contener 11 dígitos.")

            # Check if mail's format is correct
            if not is_email_complex(correo):
                flash("El correo debe estar en un formato correcto. Ejemplo: 'example@example.com'", "warning")
                raise Exception("El correo no tiene un formato adecuado.")

            # Check if the user exists
            cursor.execute("SELECT RUT FROM User WHERE RUT = %s", (user_rut,))
            if cursor.fetchone() is None:
                cursor.close()
                flash("Usuario no encontrado", "warning")
                return redirect(url_for("index"))

            # Update the user's data
            update_query = """
                UPDATE User
                SET nombre = %s, correo = %s, telefono = %s, direccion = %s
                WHERE RUT = %s
            """
            cursor.execute(update_query, (nombre, correo, formatted_telefono, direccion, user_rut))
            mysql.connection.commit()
            cursor.close()
            session["username"] = nombre
            
            flash(f"Los datos del usuario han sido actualizados", "success")
            return redirect(url_for("mi_cuenta"))

        except Exception as e:
            print("Error al actualizar el usuario:", e)
            flash("Error al actualizar el usuario", "warning")
            return redirect(url_for("mi_cuenta"))
        
        
if __name__ == "__main__":
    app.run(debug=True)
