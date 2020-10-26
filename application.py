import config
from src import create_app

app = create_app(config.DevelopmentConfig)


@app.route("/")
def health_check():
    return {"message": "API server is live!"}


from src.services.jwt import jwt
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    from src.models.revoked_tokens import RevokedToken
    jti = decrypted_token['jti']
    revoked_token = RevokedToken.objects(jti=jti).first()
    return revoked_token is not None


if __name__ == '__main__':
    app.run(debug=True)
