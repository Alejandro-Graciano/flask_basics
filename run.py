from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(
    __name__
)  # creamos un instance de la class (una variable), aquí pasamos un argumento (__name__)

app.config.update(  # un diccionario de configuración de flask
    SECRET_KEY="admin",
    SQLALCHEMY_DATABASE_URI="postgresql://postgres:admin@localhost/catalog_db",
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)  # configuraciones por defecto

db = SQLAlchemy(
    app
)  # asi dejamos saber que trabajamos con una base de datos y pasamos el instance 'app' como argumento. Creamos un instance "db" de la clase SQLAlchemy.


@app.route("/index")  # ruta alterna
@app.route("/")  # route
def hello_flask():  # lo que se ejecuta
    return "Hello World, Alejo!"


@app.route("/new/")
def query_strings(greeting="Hello"):  # valor default, hay que agregarlo al query_val
    query_val = request.args.get("greeting", greeting)
    # "greeting" es el key, greeting es la variable con el valor por defecto = "Hello"
    # .get es un metodo de diccionario, lo que hace es tomar el value del key "greeting" y se lo asigna a la variable query_val
    # request.arg es un metodo de query objects
    # ejemplo ?greeting=hola alejo.
    return "<h1> The greeting is :{0} </h1>".format(query_val)


@app.route("/user")
@app.route("/user/<name>")  # lo que esta entre angular brakets se toma como variable
def no_query_string(
    name="mina",
):  # cuando se usa esta forma, es necesario pasar la variable a la función.
    return "<h1>Hello there! {} </h1>".format(name)


# strings
@app.route("/text/<string:name>")  # definimos la variable como un string
def working_with_strings(name):  # pasar la variable a la funcion
    return "<h1> here is a string: " + name + "</h1>"  # retornar un hatml al browser


# numbers
@app.route("/numbers/<int:num>")
def working_with_numbers(num):
    return (
        "<h1> the number you picked is: " + str(num) + "</h1>"
    )  # hay que convertir a "num" en un str, si no, habrá un error en el browser


# Numbers 2
@app.route("/add/<int:num1>/<int:num2>")  # dos entradas como int
def adding_integers(num1, num2):
    return (
        "<h1> the sum is: {}".format(num1 + num2) + "</h1>"
    )  # no hay que convertirlos a str porque el metodo .format() lo hace por defecto


# Floats
@app.route("/product/<float:num1>/<float:num2>")
def product_two_numbers(num1, num2):
    return (
        "<h1> the product is: {}".format(num1 * num2) + "</h1>"
    )  # muy similar al anterior, pero si se ingresa un int, se genera un error


# VIDEO 11

# Using Templates
@app.route("/temp")
def using_templates():
    return render_template(
        "Hello.html"
    )  # llama a la pagina, por defecto debe estar en la carpeta templates


# VIDEO 12
# Jinja templates
@app.route("/watch")
def top_movies():
    movie_list = [
        "autopsy of jane doe",
        "neon demon",
        "ghost in a shell",
        "kong: skull island",
        "john wick 2",
        "spiderman - homecoming",
    ]

    return render_template(
        "movies.html", movies=movie_list, name="Harry"
    )  # los argumentos del metodo son la URL y dos variables, en este caso, una lista y un nombre


# VIDEO 13
# JINJA TEMPLATES 2
@app.route("/tables")
def movies_plus():
    movies_dict = {
        "autopsy of jane doe": 2.14,
        "neon demon": 3.20,
        "ghost in a shell": 1.50,
        "kong: skull island": 3.50,
        "john wick 2": 2.52,
        "spiderman - homecoming": 1.48,
    }

    return render_template(
        "table_data.html", movies=movies_dict, name="Sally"
    )  # el diccionario, y el nombre son enviados como argumentos a la pagina HTML


# VIDEO 15
# JINJA2 - FILTERS
@app.route("/filters")
def filter_data():
    movies_dict = {
        "autopsy of jane doe": 2.14,
        "neon demon": 3.20,
        "ghost in a shell": 1.50,
        "kong: skull island": 3.50,
        "john wick 2": 2.52,
        "spiderman - homecoming": 1.48,
    }

    return render_template(
        "filter_data.html", movies=movies_dict, name=None, film="a christmas carol"
    )  # el diccionario, y el nombre son enviados como argumentos a la pagina HTML


# VIDEO 16
# JINJA2 - MACROS
@app.route("/macros")
def jinja_macros():
    movies_dict = {
        "autopsy of jane doe": 2.14,
        "neon demon": 3.20,
        "ghost in a shell": 1.50,
        "kong: skull island": 3.50,
        "john wick 2": 2.52,
        "spiderman - homecoming": 1.48,
    }

    return render_template("using_macros.html", movies=movies_dict)


# VIDEO 20
# PUBLICATION TABLE
class Publication(db.Model):  # accedemos al metodo Model de la instance db
    __tablename__ = "publication"  # publication es el nombre de la nueva tabla

    id = db.Column(db.Integer, primary_key=True)  # culumna 1 en un instance de db
    name = db.Column(
        db.String(80), nullable=False
    )  # columna 2 en un instance de db con un string de maximo 80 caracteres

    def __init__(
        self, name
    ):  # inicializamos lo creado (eliminamos id para que sea automatico)
        # self.id = id  # damos el valor de la columna id
        self.name = name

    def __repr__(self):
        return "Publisher is {}".format(self.name)


# VIDEO 22
# BOOK TABLE
class Book(db.Model):
    __tablename__ = "book"

    id = db.Column(db.Integer, primary_key=True)  # no esta abajo
    title = db.Column(db.String(500), nullable=False, index=True)
    author = db.Column(db.String(350))
    avg_rating = db.Column(db.Float)
    format = db.Column(db.String(50))
    image = db.Column(db.String(100), unique=True)
    num_pages = db.Column(db.Integer)
    pub_date = db.Column(db.DateTime, default=datetime.utcnow())  # Este no esta abajo

    # ESTABLISH A RELATIONSHIP BETWEEN PUBLICATION AND BOOK TABLES
    pub_id = db.Column(db.Integer, db.ForeignKey("publication.id"))

    def __init__(
        self, title, author, avg_rating, book_format, image, num_pages, pub_id
    ):

        self.title = title
        self.author = author
        self.avg_rating = avg_rating
        self.format = book_format
        self.image = image
        self.num_pages = num_pages
        self.pub_id = pub_id

    def __repr__(self):
        return "{} by {}".format(self.title, self.author)


if __name__ == "__main__":  # esta parte ejecuta la aplicación
    db.create_all()
    app.run(debug=True, port=8080)
