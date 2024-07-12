from flask_restx import Api

from .predict import api as api_predict
from .predict_batch_file import api as api_predict_batch_file
from .predict_batch_link import api as api_predict_batch_link
from .csrf import api as api_csrf
from .login import api as api_login
from .register import api as api_register
from .profile import api as api_profile
from .history import api as api_history
api = Api(
    title='BrainHealth API',
    version='1.0',
    doc='/api/documentation/'
)

api.add_namespace(api_predict)
api.add_namespace(api_predict_batch_file)
api.add_namespace(api_predict_batch_link)
api.add_namespace(api_csrf)
api.add_namespace(api_login)
api.add_namespace(api_register)
api.add_namespace(api_profile)
api.add_namespace(api_history)
