from datetime import datetime
from hashlib import md5
from time import time
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from app import db, login
from datetime import datetime


class Bookings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(256))
    start_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    end_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    price = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    tasker_id = db.Column(db.Integer, db.ForeignKey('taskers.id'))
    tasker = db.relationship('Taskers')
    user = db.relationship('Users')
    review = db.relationship('Reviews', lazy=False)

    def __repr__(self):
        return '<Booking {}>'.format(self.body)


class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    nborhood = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))
    img_url = db.Column(db.String(512))
    first_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))
    address = db.Column(db.String(256))
    phone = db.Column(db.String(32))
    reviews = db.relationship('Reviews', backref='reviewer', lazy='dynamic')
    bookings = db.relationship('Bookings', backref='booker', lazy='dynamic')

    tasker = db.relationship('Taskers', backref='tasker')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def get_user_id(self, username):
        return self.query.filter_by(username=username).first()

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size=16):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    # def follow(self, user):
    #     if not self.is_following(user):
    #         self.followed.append(user)
    #
    # def unfollow(self, user):
    #     if self.is_following(user):
    #         self.followed.remove(user)
    #
    # def is_following(self, user):
    #     return self.followed.filter(
    #         followers.c.followed_id == user.id).count() > 0

    def my_reviews(self):
        return self.reviews.order_by(Reviews.timestamp.desc())

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'],
            algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return Users.query.get(id)

    def __repr__(self):
        return '<User {}>'.format(self.username)


@login.user_loader
def load_user(id):
    return Users.query.get(int(id))


def get_taskers_in_nborhood(nborhood):
    return db.session.query(Taskers) \
        .join(Users) \
        .filter(Users.nborhood == nborhood) \
        .order_by(Taskers.cname)


def get_old_bookings(user_id):
    return db.session.query(Bookings).join(Users).filter(Users.id == user_id) \
        .filter(Bookings.end_time < datetime.utcnow())


def get_new_bookings(user_id):
    return db.session.query(Bookings).join(Users).filter(Users.id == user_id) \
        .filter(Bookings.end_time >= datetime.utcnow())


def get_taskers_in_category_and_nborhood(category, nborhood, order_by):
    return db.session.query(Taskers) \
        .join(Serving_areas) \
        .join(Users) \
        .filter(Taskers.category == category) \
        .filter(Users.nborhood == nborhood) \
        .order_by(order_by)


def get_taskers_in_category(self, category):
    return db.session.query \
        .filter(Taskers.category == category) \
        .order_by(Taskers.cname)


class Taskers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    cname = db.Column(db.String(64), unique=True)
    description = db.Column(db.String(256))
    category = db.Column(db.String(128))
    price_per_hour = db.Column(db.Integer)
    user = db.relationship('Users', backref='user')
    reviews = db.relationship('Reviews', backref='reviewee', lazy='dynamic')
    bookings = db.relationship('Bookings', backref='bookee', lazy='dynamic')
    serving_areas = db.relationship('Serving_areas', backref='server', lazy='dynamic')

    def get_taskers_in_nborhood(self, nborhood):
        return self.query.join(Serving_areas).filter(Serving_areas.nborhood == nborhood).order_by(Taskers.cname)

    def get_taskers_in_category(self, category):
        return self.query.filter(Taskers.category == category).order_by(Taskers.cname)

    def get_taskers_in_category_and_nborhood(self, category, nborhood):
        return self.query(Taskers) \
            .join(Serving_areas) \
            .join(Users) \
            .filter(Taskers.category == category) \
            .filter(Users.nborhood == nborhood) \
            .order_by(Taskers.cname)

    def __repr__(self):
        return '<Tasker {}>'.format(self.cname)


class Reviews(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(512))
    overall_rating = db.Column(db.Integer)
    clean_rating = db.Column(db.Integer)
    quality_rating = db.Column(db.Integer)
    price_rating = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    tasker_id = db.Column(db.Integer, db.ForeignKey('taskers.id'))
    booking = db.relationship('Bookings')

    def __repr__(self):
        return '<Review {}>'.format(self.body)


class Serving_areas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tasker_id = db.Column(db.Integer, db.ForeignKey('taskers.id'))
    nborhood = db.Column(db.String(128))
    tasker = db.relationship('Taskers')

    def __repr__(self):
        return '<Serving_areas {}>'.format(self.body)


class All_nborhoods(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))

    def __repr__(self):
        return '{0}'.format(self.name)


class All_categories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))

    def __repr__(self):
        return '{0}'.format(self.name)
