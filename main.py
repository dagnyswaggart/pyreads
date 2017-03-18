#!/usr/bin/env python

from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
app.config['SECRET_KEY'] = 'development'

db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=True)
    author = db.Column(db.String(50))
    page_count = db.Column(db.Integer)

    def __init__(self, title, author, page_count):
        self.title = title
        self.author = author
        self.page_count = page_count

    def __repr__(self):
        return '<Book {}>'.format(self.title)

@app.route('/', methods=['GET'])
def index():
    books = Book.query.all()
    total_count = page_count(books)
    books_count = len(books)
    return render_template('index.html', books=books, page_count=total_count, books_count=books_count)

@app.route('/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'GET':
        return render_template('addbook.html')
    else:
        book = Book(request.form['title'], request.form['author'], int(request.form['pagecount']))
        db.session.add(book)
        db.session.commit()
        return redirect(url_for('index'))

def page_count(books):
    total_count = 0

    for book in books:
        total_count += book.page_count
    
    return total_count

if __name__ == '__main__':
    app.run()
