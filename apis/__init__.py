from flask_restx import Api

from .predict import api as api_predict
from .predict_batch_file import api as api_predict_batch_file
from .predict_batch_link import api as api_predict_batch_link

api = Api(
    title='BrainHealth API',
    version='1.0',
    doc='/api/documentation/'
)

api.add_namespace(api_predict)
api.add_namespace(api_predict_batch_file)
api.add_namespace(api_predict_batch_link)
