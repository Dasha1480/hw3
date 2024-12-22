from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship

db = SQLAlchemy()



class Tag(db.Model):

    __tablename__ = "Tags"
    article_id = db.Column('ID_article', db.Integer, ForeignKey('Title_body.ID_article'), primary_key=True)
    tags_name = db.Column('Tags', db.Text)


class Categories(db.Model):

    __tablename__ = "Categories"
    article_id = db.Column('ID_article', db.Integer, ForeignKey('Title_body.ID_article'), primary_key=True)
    categorie_name = db.Column('Categories', db.Text)


class Author(db.Model):

    __tablename__ = "Author"
    author_id = db.Column('ID_author', db.Integer, primary_key=True)
    author_name = db.Column('Name_author', db.Text)


class Time(db.Model):

    __tablename__ = "Time"
    author_id = db.Column('ID_author', db.Integer, ForeignKey('Time.ID_author'), primary_key=True)  #, primary_key=True)
    article_id = db.Column('ID_article', db.Integer, ForeignKey('Title_body.ID_article'))
    time_column = db.Column('Time', db.Text)


class Title_body(db.Model):

    __tablename__ = "Title_body"
    article_id = db.Column('ID_article', db.Integer, primary_key=True)
    title = db.Column('Title', db.Text)
    body = db.Column('Body', db.Text)
