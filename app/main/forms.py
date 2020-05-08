from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, BooleanField, SubmitField, SelectField, TextAreaField, DateTimeField, DateField
from app.models import All_nborhoods, All_categories
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Optional
from wtforms.fields.html5 import DateTimeLocalField, DateField



from app import create_app
app = create_app()
app.app_context().push()


class BecomePalForm(FlaskForm):
    cname = StringField('Company name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    category = SelectField(label='Category', choices=[(x.name, x.name) for x in All_categories.query.all()], validators=[DataRequired()])
    submit = SubmitField('Register as Pal')


class PalProfileForm(FlaskForm):
    nborhood = SelectField(label='Neighborhood', choices=[(x.name, x.name) for x in All_nborhoods.query.all()])
    submit = SubmitField('Add neighborhood to your serving areas')

class BookPalForm(FlaskForm):
    # id | description | start_time | end_time | user_id | tasker_id | price
    start_day = DateField('Date of booking', validators=[DataRequired()])
    start_time = SelectField('Start time', choices=[('{:02d}:00'.format(x), '{:02d}:00'.format(x)) for x in range(24)],
                             validators=[Optional()])
    end_time = SelectField('End time', choices=[('{:02d}:00'.format(x), '{:02d}:00'.format(x)) for x in range(24)],
                           validators=[Optional()])
    description = TextAreaField('Description', validators=[Optional()])
    submit = SubmitField('Book the pal')

class ReviewPalForm(FlaskForm):
    # id | body | overall_rating | clean_rating | quality_rating | price_rating | timestamp | user_id | tasker_id | booking_id
    overall_rating = SelectField('Overall rating', choices=[(x, x) for x in range(11)], coerce=int)
    clean_rating = SelectField('Clean rating', choices=[(x, x) for x in range(11)], coerce=int)
    quality_rating = SelectField('Quality rating', choices=[(x, x) for x in range(11)], coerce=int)
    price_rating = SelectField('Price rating', choices=[(x, x) for x in range(11)], coerce=int)
    body = TextAreaField('Review body')
    submit = SubmitField('Review booking')


class FindPalForm(FlaskForm):
    nborhood = SelectField(label='Neighborhood', choices=[(x.name, x.name) for x in All_nborhoods.query.all()])
    category = SelectField(label='Category', choices=[(x.name, x.name) for x in All_categories.query.all()])
    order = SelectField(label="Order by", choices=[("1", 'Popularity'), ("2", 'Alphabetically (asc)'),
                                                   ("3", 'Price per hour (asc)')], validators=[Optional()])
    submit = SubmitField('Search pals in neighborhood')


class EditUserProfileForm(FlaskForm):
    nborhood = SelectField(label='Neighborhood', choices=[(x.name, x.name) for x in All_nborhoods.query.all()])
    submit = SubmitField('Save profile changes')


# from wtforms.ext.sqlalchemy.fields import QuerySelectField
#
#
# class QueryAllNeighborhoods(FlaskForm):
#     nborhood = QuerySelectField(
#         'Choose neighborhood',
#         query_factory=lambda: All_nborhoods.query,
#         get_label='name', get_pk=lambda a: a.name,
#         blank_text=u'Select a neighborhood...'
#     )
#     submit = SubmitField('Save profile changes')

