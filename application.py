from app import create_app, db
from app.models import Users, Taskers, Reviews, Serving_areas, Bookings, All_nborhoods, All_categories

application = create_app()

@application.shell_context_processor
def make_shell_context():
    return {'db': db, 'Users': Users, 'Taskers': Taskers,
            'Reviews': Reviews, 'Serving_areas': Serving_areas, 'Bookings': Bookings,
            'All_nborhoods': All_nborhoods, 'All_categories': All_categories}


# run the app.
if __name__ == "__main__":
    # Setting debug to False disables debug output. This line should be
    # removed before deploying a production app.
    application.debug = False
    application.run()
