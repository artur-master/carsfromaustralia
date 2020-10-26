"""Flask app config and initialization"""
import logging.config
from flask import Flask


def create_app(config_obj=None):

    app = Flask(__name__)

    if not config_obj:
        logging.warning("No config specified; defaulting to development")

        import config
        config_obj = config.DevelopmentConfig

    app.config.from_object(config_obj)

    # CORS allow
    from flask_cors import CORS
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    """MongoDB service"""
    from src.services.db import db
    db.init_app(app)

    ''' JWT service '''
    from src.services.jwt import jwt
    jwt.init_app(app)

    # Router service
    from src.routes import api_router
    api_router.init_app(app)

    from src.resources.auth import SignInResource, SignUpResource, SignOutResource, TokenRefreshResource
    api_router.add_resource(SignInResource, "/auth/sign-in/", methods=['POST'])
    api_router.add_resource(SignUpResource, "/auth/sign-up/", methods=['POST'])
    api_router.add_resource(SignOutResource, "/auth/sign-out/", methods=['POST'])
    api_router.add_resource(TokenRefreshResource, "/auth/refresh/", methods=['POST'])

    from src.resources.profile import GetProfileResource, UpdateProfileResource
    api_router.add_resource(GetProfileResource, "/profile/", methods=['GET'])
    api_router.add_resource(UpdateProfileResource, "/profile/", methods=['PUT'])

    '''from src.resources.profile import PasswordResetResource
    api_router.add_resource(PasswordResetResource, "/profile/password-reset")

    from src.resources.profile import CloseAccountResource
    api_router.add_resource(CloseAccountResource, "/profile/close-account")'''

    from src.resources.users import GetUserResource, GetUsersResource, UpdateUserResource, DeleteUserResource
    api_router.add_resource(GetUsersResource, "/users/", methods=['GET'])
    api_router.add_resource(GetUserResource, "/users/<id>/", methods=['GET'])
    api_router.add_resource(UpdateUserResource, "/users/<id>/", methods=['PUT'])
    api_router.add_resource(DeleteUserResource, "/users/<id>/", methods=['DELETE'])

    from src.resources.cars import GetCarResource, GetCarsResource
    api_router.add_resource(GetCarsResource, "/cars/", methods=['GET'])
    api_router.add_resource(GetCarResource, "/cars/<id>/", methods=['GET'])

    api_router.register_routes()

    return app
