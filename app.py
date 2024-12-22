import datetime
import math
import time

from flask import Flask, render_template, request, redirect, url_for
from mod import db, Tag, Categories, Author, Time, Title_body  # Film, Person, db, Rating, Type, Genre, FilmGenres

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db_author.db'  # imdb_very_small.db
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///audio_db.db'  # imdb_very_small.db
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///imdb_very_small.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.app = app
db.init_app(app)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/statistic')
def search():
    # film_types = Type.query.all()
    # genre_types = Genre.query.all()
    # data = {"film_types": film_types,
    #         "genre_types": genre_types}
    time_data = Time.query.all()
    author_data = Author.query.all()
    data = {'time_data': time_data, 'author_data': author_data}

    return render_template("statistic.html", data=data)


# @app.route('/results')
def results():
    if request.values:
        search_result = db.session.query(Film)\
            .join(Rating) \
            .join(FilmGenres) \
            .filter(
                Film.film_type_id == request.values.get("film_type", int),
                Rating.votes > request.values.get("min_votes", int),
                Rating.value > request.values.get("min_rating", float),
                FilmGenres.genre_id == request.values.get("genre", int),
            )
        sorting = request.values.get("sort")
        if sorting == "rating":
            search_result = search_result.order_by(-Rating.value)
        elif sorting == "year":
            search_result = search_result.order_by(-Film.premiered)
        else:
            search_result = search_result.order_by(-Rating.votes)
        search_result = search_result.limit(250).all()
    else:
        search_result = []
    return render_template("results.html", results=search_result)


# @app.route("/film/<film_id>")
# def film_page(film_id):
#     film = Film.query.get(film_id)
#     return render_template("film.html", film=film)
#
#
# @app.route("/person/<person_id>")
# def person_page(person_id):
#     person = Person.query.get(person_id)
#     return render_template("person.html", person=person)


@app.route("/anketa")
# def rating():
    # rating = Film.query.limit(250).all() # .order_by(Film.rating.value)
    # rating = db.session.query(Film)\
    #     .join(Rating)\
    #     .filter(Rating.votes > 100000)\
    #     .order_by(-Rating.value)\
    #     .limit(250).all()
    # return render_template("anketa.html", rating=rating)
def anketa():
    data = {}

    return render_template("anketa.html", data=data)


@app.route("/addStr")
def addStr(self, title, text, url):
    try:
        self.__cur.execute("SELECT COUNT() as `count` FROM posts WHERE url LIKE ?", (url,))
        res = self.__cur.fetchone()
        if res['count'] > 0:
            print("Статья с таким url уже существует")
            return False

        tm = math.floor(time.time())
        self.__cur.execute("INSERT INTO posts VALUES(NULL, ?, ?, ?, ?)", (title, text, url, tm))
        self.__db.commit()
    except TypeError as e:
        print("Ошибка добавления статьи в БД " + str(e))
        return False

    return True


@app.route('/process', methods=["GET"])
def process():

    # если пустой запрос, то отправить проходить анкету
    if not request.args:
        return redirect(url_for('anketa'))
    # получаем значения ответов
    author = request.args.get('author')
    title = request.args.get('title')
    text = request.args.get('post')

    # записываем в базу
    post = Title_body(
        title=title,
        body=text
    )

    db.session.add(post)
    db.session.commit()

    # обновляем user'a, чтобы его ответ записать с таким же id
    db.session.refresh(post)
    id_article = post.article_id
    # это же делаем с ответом
    # q1 = request.args.get('q1')
    # q2 = request.args.get('q2')
    # db.session.expire_all()
    # db.session.commit()
    # db.session.rollback()

    auth = Author(
        # author_id=555,
        author_name=author
    )
    # answer = Answers(
    #     id_user=user.id_user,
    #     ans_q1=q1,
    #     ans_q2=q2
    # )
    print('---start 2 ---', author)
    db.session.add(auth)
    # db.session.commit()

    # db.session.refresh(auth)

    if auth.author_id:
        id_auth = auth.author_id
    else:
        id_auth = post.article_id
    print(f'{id_auth=}')

    time_ = Time(
        author_id=id_auth,
        article_id=id_article,
        time_column=datetime.datetime.now().strftime('%d-%m-%Y')
    )

    db.session.add(time_)

    db.session.commit()
    # пользователь попадает на страницу с текстом
    return 'Новость добавлена, дата: ' + str(datetime.datetime.now().strftime('%d-%m-%Y'))


if __name__ == '__main__':
    app.run(debug=True)
