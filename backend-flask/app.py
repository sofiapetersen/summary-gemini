from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import os
from dotenv import load_dotenv
import google.generativeai as genai
from routes.auth import register_auth_routes
from routes.summary import register_summary_routes
from werkzeug.security import generate_password_hash, check_password_hash


load_dotenv() 

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
db = SQLAlchemy(app) # Inicializa db

# Configuração JWT
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
jwt = JWTManager(app) 

# Configuração CORS 
CORS(app) 

# Configuração do Gemini API 
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
model = None 
try:
    if GOOGLE_API_KEY: 
        genai.configure(api_key=GOOGLE_API_KEY)
        model = genai.GenerativeModel('gemini-2.0-flash') 
    else:
         print("Aviso: GOOGLE_API_KEY não configurada. Funcionalidade de resumo com IA estará desabilitada.")

except Exception as e:
    print(f"Erro ao inicializar o modelo Gemini: {e}")
    model = None


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password) 

    def check_password(self, password):
        return check_password_hash(self.password_hash, password) 

    def __repr__(self):
        return f'<User {self.username}>'


# Registro das Rotas
register_auth_routes(app, db, jwt, User)
register_summary_routes(app, jwt, model)


if __name__ == '__main__':

    app.run(debug=True, port=5000) # Rodando na porta 5000 por padrão