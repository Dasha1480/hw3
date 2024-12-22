import datetime
import math
import time

from flask import Flask, render_template, request, redirect, url_for
from mod import db, Tag, Categories, Author, Time, Title_body  # Film, Person, db, Rating, Type, Genre, FilmGenres

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db_author.db'  # поднлючение к бд
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.app = app
db.init_app(app)


@app.route('/')  # переход на главную
def index():
    return render_template("index.html")


@app.route('/statistic')  # страница статистики
def search():
    time_data = Time.query.all()
    author_data = Author.query.all()
    data = {'time_data': time_data, 'author_data': author_data}

    return render_template("statistic.html", data=data)


@app.route("/anketa")  # анкета для сбора новостей
def anketa():
    data = {}

    return render_template("anketa.html", data=data)


@app.route('/process', methods=["GET"])  # обработка данных с анкеты
def process():

    # если пустой запрос, то отправляем проходить анкету снова
    if not request.args:
        return redirect(url_for('anketa'))
    # получаем значения ответов
    author = request.args.get('author')
    title = request.args.get('title')
    text = request.args.get('post')
    tags = request.args.get('tag')
    cat_s = request.args.get('cat')

    # записываем в базу
    post = Title_body(
        title=title,
        body=text
    )

    db.session.add(post)
    db.session.commit()

    # обновляем новость, чтобы её номер записать с таким же id
    db.session.refresh(post)
    id_article = post.article_id
    # не отрабатывают, увы
    # db.session.expire_all()
    # db.session.commit()
    # db.session.rollback()

    # Добавляем данные в таблицы
    tag_s = Tag(
        article_id=id_article,
        tags_name=tags
    )
    db.session.add(tag_s)

    categorie_s = Categories(
        article_id=id_article,
        categorie_name=cat_s
    )
    db.session.add(categorie_s)

    auth = Author(
        author_name=author
    )
    db.session.add(auth)
    # db.session.commit()
    # db.session.refresh(auth)

    # проверка id автора
    if auth.author_id:
        id_auth = auth.author_id
    else:
        id_auth = post.article_id


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
