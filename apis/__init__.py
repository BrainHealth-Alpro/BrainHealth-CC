from flask_restx import Api

from .predict import api as api_predict

api = Api(
    title='BrainHealth API',
    version='1.0',
    doc='/api/documentation/'
)

api.add_namespace(api_predict, path='/api/predict')