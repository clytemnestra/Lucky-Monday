from flask import Blueprint

application = Blueprint('application', __name__, template_folder='templates', static_folder='static')


@application.route('/')
def home():
    return 'asd'
    pass
