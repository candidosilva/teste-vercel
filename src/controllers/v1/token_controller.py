from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import create_access_token

from src.models.token_qrcode_model import TokenModel

blp = Blueprint("Token Qr Code", __name__, description="Criação do Qr Code com Token")

@blp.route("/create-token")
class Token(MethodView):
    @blp.arguments(TokenModel)
    @blp.response(200, TokenModel)
    def post(self, token_data):
        try:   
            token = create_access_token(identity=token_data["id"], additional_claims={"ibm": token_data["ibm"]}, expires_delta=False)
            return {
                "token": token
            }
        
        except KeyError:
            abort(500, message="Error creating the token.")