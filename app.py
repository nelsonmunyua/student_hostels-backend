from flask import Flask
from flask_migrate import Migrate
from models import db
from flask_restful import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from resouces.user import Signup, Signin, RefreshToken


# initialize flask app
app = Flask(__name__)

# configure db URI
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///student_hostel.db"

app.config["SQLALCHEMY_ECHO"] = True

app.config["BUNDLE_ERRORS"] = True

# Setup flask-JWT-extended extension
app.config["JWT_SECRET_KEY"] = '123456789'

JWT_ACCESS_TOKEN_EXPIRES = 900        # 15 minutes
JWT_REFRESH_TOKEN_EXPIRES = 86400 * 7 # 7 days



# link migration
migrate = Migrate(app, db)

# initialize db
db.init_app(app)

# initialize flask restful
api = Api(app)

# initialize bcrypt 
bcrypt = Bcrypt(app)

# initialize jwt
jwt = JWTManager(app)


@app.route('/')
def index():
    return {"Message": "Student-hostel server running"}


# routes 
api.add_resource(Signup, '/signup')
api.add_resource(Signin, '/signin')
api.add_resource(RefreshToken, "/auth/refresh")









if __name__ == "__main__":
    app.run(port=5000, debug=True)