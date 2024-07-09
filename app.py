from flask import Flask
from flask_smorest import Api
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from src.controllers.v1.store_controller import blp as StoreBlueprint
from src.controllers.v1.register_controller import blp as RegisterBlueprint
from src.controllers.v1.tab_controller import blp as TabBlueprint
from src.controllers.v1.token_controller import blp as TokenBlueprint
from src.controllers.v1.pos_controller import blp as POSBlueprint
from src.controllers.v1.app_controller import blp as APPBlueprint

app = Flask(__name__)

app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["API_TITLE"] = "Self Checkout REST API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

api = Api(app)

app.config["JWT_SECRET_KEY"] = "senha_super_secreta"
jwt = JWTManager(app)

api.register_blueprint(StoreBlueprint)
api.register_blueprint(RegisterBlueprint)
api.register_blueprint(TabBlueprint)
api.register_blueprint(TokenBlueprint)
api.register_blueprint(POSBlueprint)
api.register_blueprint(APPBlueprint)

CORS(app, supports_credentials= True)

if __name__ == "__main__":
    app.run(port=80, debug=True)