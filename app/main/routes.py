from flask import render_template, flash, redirect, url_for
from wtforms import ValidationError

from app.main.forms import BecomePalForm, PalProfileForm, EditUserProfileForm, FindPalForm, BookPalForm, ReviewPalForm
from flask_login import current_user, login_required
from app.models import Users, Taskers, Serving_areas, Bookings, \
    All_nborhoods, get_taskers_in_nborhood, \
    get_taskers_in_category_and_nborhood, get_new_bookings, get_old_bookings, Reviews
from app import db
from app.main import bp
from flask import send_from_directory
import os
from datetime import datetime


@bp.route('/favicon.ico')
def favicon():
    favicon_path = os.path.join(bp.root_path, 'static')
    print(favicon_path)
    return send_from_directory(favicon_path,
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = EditUserProfileForm(nborhood=current_user.nborhood)
    # if not form.nborhood.data:
    #     form.nborhood.data = current_user.nborhood
    old_bookings = get_old_bookings(current_user.id)
    new_bookings = get_new_bookings(current_user.id)
    if form.validate_on_submit():
        user = Users.query.filter_by(id=current_user.id).first()
        user.nborhood = form.nborhood.data
        db.session.commit()
        flash('User profile data updated!', 'success')
        return redirect(url_for('main.index'))
    return render_template('index.html', title='Home', user=current_user, old_bookings=old_bookings, new_bookings=new_bookings, form=form)


@bp.route('/book_pal/<id>', methods=['GET', 'POST'])
@login_required
def book_pal(id):
    form = BookPalForm(start_time=datetime.now(), end_time=datetime.now())
    tasker = Taskers.query.filter_by(id=id).first()
    # id | description | start_time | end_time | user_id | tasker_id | price
    if form.validate_on_submit():
        total_hours = int(form.end_time.data.split(':')[0]) - int(form.start_time.data.split(':')[0])
        if total_hours < 0:
            flash('Start time of booking must be less than end time', 'error')
            return redirect(url_for('main.book_pal', id=id))
        start_time = datetime.strptime(str(form.start_day.data) + ' ' + form.start_time.data, '%Y-%m-%d %H:%M')
        end_time = datetime.strptime(str(form.start_day.data) + ' ' + form.end_time.data, '%Y-%m-%d %H:%M')
        booking = Bookings(description=form.description.data,
                           start_time=start_time,
                           end_time=end_time,
                           price=total_hours*tasker.price_per_hour,
                           user_id=current_user.id,
                           tasker_id=tasker.id
                           )
        db.session.add(booking)
        db.session.commit()
        flash('User profile data updated!', 'success')

        return redirect(url_for('main.index'))
    return render_template('book_pal.html', title='Book Pal', form=form, tasker=tasker)


@bp.route('/review_booking/<id>', methods=['GET', 'POST'])
@login_required
def review_pal(id):
    form = ReviewPalForm()
    booking = Bookings.query.filter_by(id=id).first()
    if form.validate_on_submit():
        review = Reviews(body=form.body.data,
                         overall_rating=form.overall_rating.data,
                         clean_rating=form.clean_rating.data,
                         price_rating=form.price_rating.data,
                         quality_rating=form.quality_rating.data,
                         timestamp=datetime.now(),
                         booking_id=booking.id,
                         tasker_id=booking.tasker_id,
                         user_id=booking.user_id)
        db.session.add(review)
        db.session.commit()
        flash('Your review has been added!', 'success')
        return redirect(url_for('main.index'))
    return render_template('review_booking.html', title='Review booking', form=form, booking=booking)


@bp.route('/show_pal_reviews/<id>')
@login_required
def show_review(id):
    tasker = Taskers.query.filter_by(id=id).first()
    return render_template('show_review.html', title='Reviews', tasker=tasker)

@bp.route('/become_pal', methods=['GET', 'POST'])
@login_required
def become_pal():
    form = BecomePalForm()
    if form.validate_on_submit():
        tasker = Taskers(user_id=current_user.id, cname=form.cname.data
                         , description=form.description.data
                         , category=form.category.data)
        db.session.add(tasker)
        db.session.commit()
        flash('Congratulations, you are now a pal! Get ready to do some work!', 'success')
        return redirect(url_for('main.index'))
    return render_template('basic_form.html', title='Become Pal', form=form)


@bp.route('/find_pal', methods=['GET', 'POST'])
@login_required
def find_pal():
    form = FindPalForm(nborhood=current_user.nborhood, category="cleaner")
    taskers = None
    if not form.nborhood.data:
        form.nborhood.data = current_user.nborhood
        flash('You are seeing all taskers in your neighborhood {}'.format(form.nborhood.data), 'info')
        taskers = get_taskers_in_nborhood(current_user.nborhood)
    if form.validate_on_submit():
        if form.order.data == "1":
            order_by = Taskers.price_per_hour.desc()
        elif form.order.data == "2":
            order_by = Taskers.cname.asc()
        elif form.order.data == "3":
            order_by = Taskers.price_per_hour.asc()
        taskers = get_taskers_in_category_and_nborhood(form.category.data, form.nborhood.data, order_by=order_by)
        flash('You are seeing all taskers in neighborhood {}, category {}'.format(form.nborhood.data,
                                                                                  form.category.data), 'info')
    return render_template('find_pal.html', title='Find your pal', form=form, taskers=taskers)

@bp.route('/pal_profile/<id>')
@login_required
def show_pal_profile(id):
    # tasker = Taskers.query.filter_by(id=id).first()
    return render_template('not_implemented.html', title='Pal Profile')

@bp.route('/')
@bp.route('/landing_page')
def landing_page():
    # tasker = Taskers.query.filter_by(id=id).first()
    return render_template('landing-page.html', title='Pal Profile')

@bp.route('/user_profile/<id>')
@login_required
def show_user_profile(id):
    # tasker = Taskers.query.filter_by(id=id).first()
    return render_template('not_implemented.html', title='User Profile')


@bp.route('/pal_profile', methods=['GET', 'POST'])
@login_required
def pal_profile():
    form = PalProfileForm(nborhood=current_user.nborhood)
    tasker = current_user.tasker[0]
    if form.validate_on_submit():
        serving_area = Serving_areas(tasker_id=tasker.id, nborhood=form.nborhood.data)
        db.session.add(serving_area)
        db.session.commit()
        flash('Congratulations, you registered {} as a serving area!'.format(form.nborhood.data), 'success')
        return redirect(url_for('main.pal_profile'))
    return render_template('pal_profile.html', title='Pal Profile', form=form, tasker=tasker)

from flask import request

@bp.route('/pal_profile/curr_bookings', methods=['GET', 'POST'])
@login_required
def pal_curr_bookings():
    tasker = current_user.tasker[0]
    bookings = tasker.bookings.filter(Bookings.end_time >= datetime.utcnow())
    page = request.args.get('page', 1, type=int)
    bookings_pag = bookings.order_by(Bookings.start_time.desc()).paginate(
        page, 3, False)
    # next_url = url_for('main.pal_curr_bookings', page=bookings_pag.next_num) \
    #     if bookings_pag.has_next else None
    # prev_url = url_for('main.pal_curr_bookings', page=bookings_pag.prev_num) \
    #     if bookings_pag.has_prev else None
    return render_template('pal_curr_bookings.html', title='My Bookings', bookings=bookings_pag.items,
                            total_pages=bookings_pag.pages, pagination=bookings_pag)



@bp.route('/pal_profile/past_bookings', methods=['GET', 'POST'])
@login_required
def pal_past_bookings():
    tasker = current_user.tasker[0]
    bookings = tasker.bookings.filter(Bookings.end_time < datetime.utcnow())
    page = request.args.get('page', 0, type=int)
    bookings_pag = bookings.order_by(Bookings.start_time.desc()).paginate(
        page, 3, False)
    # next_url = url_for('main.pal_past_bookings', page=bookings_pag.next_num) \
    #     if bookings_pag.has_next else None
    # prev_url = url_for('main.pal_past_bookings', page=bookings_pag.prev_num) \
    #     if bookings_pag.has_prev else None
    return render_template('pal_past_bookings.html', title='My Bookings', bookings=bookings_pag.items,
                            total_pages=bookings_pag.pages, pagination=bookings_pag)