
import os
from flask import render_template, flash, redirect, url_for, request
from movies_webstore import app, db, bcrypt
from movies_webstore.forms import RegistrationForm, LoginForm
from movies_webstore.models import User
from tmdbv3api import TMDb, Movie, Discover
from flask_login import login_user, current_user, logout_user, login_required
import requests
import json

tmdb = TMDb()
tmdb.api_key = os.getenv("api_key")

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home_route():
    movie = Movie()
    return render_template('index.html', movie=movie)

@app.route('/register', methods=['GET', 'POST'])
def registration_route():
    if current_user.is_authenticated:
        return redirect(url_for('home_route'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login_route'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_route():
    if current_user.is_authenticated:
        return redirect(url_for('home_route'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.button.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home_route'))
        else:
            return render_template('login.html', form=form)
    return render_template('login.html', form=form)

@app.route('/logout')
def logout_route():
    logout_user()
    return redirect(url_for('home_route'))

@app.route('/account')
@login_required
def user_profile():
    return render_template('account.html')

@app.route("/movie/<movie_id>/", methods=['GET', 'POST'])
@login_required
def movie_route(movie_id):
    movie = Movie()
    m_detail = movie.details(movie_id)
    api_key = tmdb.api_key
    r = requests.get('https://api.themoviedb.org/3/movie/'+str(movie_id) +str('?api_key=') +str(api_key))
    j = r.json()
    genre = j['genres'][0]['name']
    return render_template('movie.html', movie=movie, m_detail=m_detail, genre=genre)

@app.route('/search/<term>', methods=['GET', 'POST'])
def search_route(term):
    movie = Movie()
    m_search = movie.search(term)
    return render_template('search.html', movie=movie, m_search=m_search)

@app.route('/category', methods=['GET', 'POST'])
def category_route():
    movie = Movie()
    discover = Discover()
    action = discover.discover_movies({'sort_by': 'popularity.desc', 'with_genres': 28, 'page': 1})
    return render_template('categories.html', movie=movie, discover=discover, action=action)

@app.route('/category/action/', methods=['GET', 'POST'])
def action_movies():
    movie = Movie()
    discover = Discover()
    action = discover.discover_movies({'sort_by': 'popularity.desc', 'with_genres': 28, 'page': 1})
    action2 = discover.discover_movies({'sort_by': 'popularity.desc', 'with_genres': 28, 'page': 2})
    movies = action
    movies2 = action2
    return render_template('category.html', movie=movie, discover=discover, movies=movies, movies2=movies2)

@app.route('/category/adventure/', methods=['GET', 'POST'])
def adventure_movies():
    movie = Movie()
    discover = Discover()
    adventure = discover.discover_movies({'sort_by': 'popularity.desc', 'with_genres': 12, 'page': 1})
    adventure2 = discover.discover_movies({'sort_by': 'popularity.desc', 'with_genres': 12, 'page': 2})
    movies = adventure
    movies2 = adventure2
    return render_template('category.html', movie=movie, discover=discover, movies=movies, movies2=movies2)

@app.route('/category/animation/', methods=['GET', 'POST'])
def animation_movies():
    movie = Movie()
    discover = Discover()
    animation1 = discover.discover_movies({'sort_by': 'popularity.desc', 'with_genres': 16, 'page': 1})
    animation2 = discover.discover_movies({'sort_by': 'popularity.desc', 'with_genres': 16, 'page': 2})
    movies = animation1
    movies2 = animation2
    return render_template('category.html', movie=movie, discover=discover, movies=movies, movies2=movies2)

@app.route('/category/comedy/', methods=['GET', 'POST'])
def comedy_movies():
    movie = Movie()
    discover = Discover()
    comedy1 = discover.discover_movies({'sort_by': 'popularity.desc', 'with_genres': 35, 'page': 1})
    comedy2 = discover.discover_movies({'sort_by': 'popularity.desc', 'with_genres': 35, 'page': 2})
    movies = comedy1
    movies2 = comedy2
    return render_template('category.html', movie=movie, discover=discover, movies=movies, movies2=movies2)

@app.route('/category/crime/', methods=['GET', 'POST'])
def crime_movies():
    movie = Movie()
    discover = Discover()
    crime1 = discover.discover_movies({'sort_by': 'popularity.desc', 'with_genres': 80, 'page': 1})
    crime2 = discover.discover_movies({'sort_by': 'popularity.desc', 'with_genres': 80, 'page': 2})
    movies = crime1
    movies2 = crime2
    return render_template('category.html', movie=movie, discover=discover, movies=movies, movies2=movies2)

@app.route('/category/documentary/', methods=['GET', 'POST'])
def documentary_movies():
    movie = Movie()
    discover = Discover()
    documentary1 = discover.discover_movies({'sort_by': 'popularity.desc', 'with_genres': 99, 'page': 1})
    documentary2 = discover.discover_movies({'sort_by': 'popularity.desc', 'with_genres': 99, 'page': 2})
    movies = documentary1
    movies2 = documentary2
    return render_template('category.html', movie=movie, discover=discover, movies=movies, movies2=movies2)

@app.route('/category/drama/', methods=['GET', 'POST'])
def drama_movies():
    movie = Movie()
    discover = Discover()
    drama1 = discover.discover_movies({'sort_by': 'popularity.desc', 'with_genres': 18, 'page': 1})
    drama2 = discover.discover_movies({'sort_by': 'popularity.desc', 'with_genres': 18, 'page': 2})
    movies = drama1
    movies2 = drama2
    return render_template('category.html', movie=movie, discover=discover, movies=movies, movies2=movies2)

@app.route('/category/family/', methods=['GET', 'POST'])
def family_movies():
    movie = Movie()
    discover = Discover()
    family1 = discover.discover_movies({'sort_by': 'popularity.desc', 'with_genres': 10751, 'page': 1})
    family2 = discover.discover_movies({'sort_by': 'popularity.desc', 'with_genres': 10751, 'page': 2})
    movies = family1
    movies2 = family2
    return render_template('category.html', movie=movie, discover=discover, movies=movies, movies2=movies2)

@app.route('/category/fantasy/', methods=['GET', 'POST'])
def fantasy_movies():
    movie = Movie()
    discover = Discover()
    fantasy1 = discover.discover_movies({'sort_by': 'popularity.desc', 'with_genres': 14, 'page': 1})
    fantasy2 = discover.discover_movies({'sort_by': 'popularity.desc', 'with_genres': 14, 'page': 2})
    movies = fantasy1
    movies2 = fantasy2
    return render_template('category.html', movie=movie, discover=discover, movies=movies, movies2=movies2)

@app.route('/category/history/', methods=['GET', 'POST'])
def history_movies():
    movie = Movie()
    discover = Discover()
    history1 = discover.discover_movies({'sort_by': 'popularity.desc', 'with_genres': 36, 'page': 1})
    history2 = discover.discover_movies({'sort_by': 'popularity.desc', 'with_genres': 36, 'page': 2})
    movies = history1
    movies2 = history2
    return render_template('category.html', movie=movie, discover=discover, movies=movies, movies2=movies2)

@app.route('/category/horror/', methods=['GET', 'POST'])
def horror_movies():
    movie = Movie()
    discover = Discover()
    horror1 = discover.discover_movies({'sort_by': 'popularity.desc', 'with_genres': 27, 'page': 1})
    horror2 = discover.discover_movies({'sort_by': 'popularity.desc', 'with_genres': 27, 'page': 2})
    movies = horror1
    movies2 = horror2
    return render_template('category.html', movie=movie, discover=discover, movies=movies, movies2=movies2)

@app.route('/category/music/', methods=['GET', 'POST'])
def music_movies():
    movie = Movie()
    discover = Discover()
    music1 = discover.discover_movies({'sort_by': 'popularity.desc', 'with_genres': 10402, 'page': 1})
    music2 = discover.discover_movies({'sort_by': 'popularity.desc', 'with_genres': 10402, 'page': 2})
    movies = music1
    movies2 = music2
    return render_template('category.html', movie=movie, discover=discover, movies=movies, movies2=movies2)

@app.route('/category/mystery/', methods=['GET', 'POST'])
def mystery_movies():
    movie = Movie()
    discover = Discover()
    mystery1 = discover.discover_movies({'sort_by': 'popularity.desc', 'with_genres': 9648, 'page': 1})
    mystery2 = discover.discover_movies({'sort_by': 'popularity.desc', 'with_genres': 9648, 'page': 2})
    movies = mystery1
    movies2 = mystery2
    return render_template('category.html', movie=movie, discover=discover, movies=movies, movies2=movies2)

@app.route('/category/romance/', methods=['GET', 'POST'])
def romance_movies():
    movie = Movie()
    discover = Discover()
    romance1 = discover.discover_movies({'sort_by': 'popularity.desc', 'with_genres': 10749, 'page': 1})
    romance2 = discover.discover_movies({'sort_by': 'popularity.desc', 'with_genres': 10749, 'page': 2})
    movies = romance1
    movies2 = romance2
    return render_template('category.html', movie=movie, discover=discover, movies=movies, movies2=movies2)

@app.route('/category/scifi/', methods=['GET', 'POST'])
def scifi_movies():
    movie = Movie()
    discover = Discover()
    scifi1 = discover.discover_movies({'sort_by': 'popularity.desc', 'with_genres': 878, 'page': 1})
    scifi2 = discover.discover_movies({'sort_by': 'popularity.desc', 'with_genres': 878, 'page': 2})
    movies = scifi1
    movies2 = scifi2
    return render_template('category.html', movie=movie, discover=discover, movies=movies, movies2=movies2)

@app.route('/category/thriller/', methods=['GET', 'POST'])
def thriller_movies():
    movie = Movie()
    discover = Discover()
    thriller1 = discover.discover_movies({'sort_by': 'popularity.desc', 'with_genres': 53, 'page': 1})
    thriller2 = discover.discover_movies({'sort_by': 'popularity.desc', 'with_genres': 53, 'page': 2})
    movies = thriller1
    movies2 = thriller2
    return render_template('category.html', movie=movie, discover=discover, movies=movies, movies2=movies2)

@app.route('/category/war/', methods=['GET', 'POST'])
def war_movies():
    movie = Movie()
    discover = Discover()
    war1 = discover.discover_movies({'sort_by': 'popularity.desc', 'with_genres': 10752, 'page': 1})
    war2 = discover.discover_movies({'sort_by': 'popularity.desc', 'with_genres': 10752, 'page': 2})
    movies = war1
    movies2 = war2
    return render_template('category.html', movie=movie, discover=discover, movies=movies, movies2=movies2)

@app.route('/category/western/', methods=['GET', 'POST'])
def western_movies():
    movie = Movie()
    discover = Discover()
    western1 = discover.discover_movies({'sort_by': 'popularity.desc', 'with_genres': 37, 'page': 1})
    western2 = discover.discover_movies({'sort_by': 'popularity.desc', 'with_genres': 37, 'page': 2})
    movies = western1
    movies2 = western2
    return render_template('category.html', movie=movie, discover=discover, movies=movies, movies2=movies2)
