from flask import Flask, jsonify

from sql_base_dao import SQLBaseDAO

app = Flask(__name__)

app.config['JSON_AS_ASCII'] = False
app.config['DEBUG'] = True
app.config['JSON_SORT_KEYS'] = False

# создание объекта SQLBaseDAO для работы с netflix.db
netflix_db = SQLBaseDAO("netflix.db")


# вьюшка для вывода фильма по названию самого свежего года выпуска
@app.route('/movie/<title>/')
def search_title(title):
    return jsonify(netflix_db.search_title(title))


# вьюшка для вывода фильмов в указанном промежутке времени
@app.route('/movie/<int:from_year>/to/<int:to_year>/')
def search_year(from_year, to_year):
    return jsonify(netflix_db.search_by_range_year(from_year, to_year))


# вьюшка для вывода фильмов выбранной категории
@app.route('/rating/<category>/')
def rating_category(category):
    if category == 'children':
        return jsonify(netflix_db.search_rating('G'))

    if category == 'family':
        return jsonify(netflix_db.search_rating('G', 'PG', 'PG-13'))

    if category == 'adult':
        return jsonify(netflix_db.search_rating('R', 'NC-17'))


# вьюшка для вывода фильмов по жанру
@app.route('/genre/<genre>')
def search_genre(genre):
    return jsonify(netflix_db.search_genre(genre))


if __name__ == '__main__':
    app.run()
