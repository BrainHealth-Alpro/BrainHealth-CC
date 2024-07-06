from flask_restx import Api

from .predict import api as api_predict
from .predict_batch_file import api as api_predict_batch_file

api = Api(
    title='BrainHealth API',
    version='1.0',
    doc='/api/documentation/'
)

api.add_namespace(api_predict, path='/api/predict')
api.add_namespace(api_predict_batch_file, path='/api/predict/batchFile')