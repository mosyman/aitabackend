from flask import Blueprint

api_bp = Blueprint('api', __name__,url_prefix='/api')

from . import users
from . import datasets
from . import news
from . import papers
from . import teamMembers
from . import cosApi
from . import model