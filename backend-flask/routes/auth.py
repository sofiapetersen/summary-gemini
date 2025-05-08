from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity


def register_auth_routes(app, db, jwt, User):
    # Registra as rotas de autenticação

    # Rota de Cadastro
    @app.route('/register', methods=['POST'])
    def register():
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'message': 'Nome de usuário e senha são obrigatórios'}), 400

        # Acessa o modelo User e a instância db passados
        if User.query.filter_by(username=username).first():
            return jsonify({'message': 'Nome de usuário já existe'}), 409 # Conflict

        new_user = User(username=username)
        new_user.set_password(password) # set_password usa generate_password_hash

        try:
            db.session.add(new_user)
            db.session.commit()
            return jsonify({'message': 'Usuário registrado com sucesso'}), 201 
        except Exception as e:
            db.session.rollback()
            print(f"Erro no registro: {e}") 
            return jsonify({'message': 'Erro ao registrar usuário', 'error': str(e)}), 500

    # Rota de Login
    @app.route('/login', methods=['POST'])
    def login():
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'message': 'Nome de usuário e senha são obrigatórios'}), 400

        # Acessa o modelo User passado
        user = User.query.filter_by(username=username).first()

        # check_password usa check_password_hash
        if user and user.check_password(password):
            # Cria o token de acesso usando a função de Flask-JWT-Extended
            access_token = create_access_token(identity=user.username)
            return jsonify(access_token=access_token), 200 # OK
        else:
            return jsonify({'message': 'Credenciais inválidas'}), 401 # Unauthorized

    # Rota Protegida
    @app.route('/protected', methods=['GET'])
    # jwt_required usa o contexto do JWTManager inicializado no app principal
    @jwt_required()
    def protected():
        current_user = get_jwt_identity() # Obtém a identidade do token
        return jsonify(logged_in_as=current_user, message='Você acessou uma rota protegida!'), 200
