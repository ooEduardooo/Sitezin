from flask import Flask, request, jsonify 
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

data_nascimento = date(2000, 1, 1)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50))
    email = db.Column(db.String(120), unique=True)
    telefone = db.Column(db.String(20))
    senha = db.Column(db.String(80))
    data_nascimento = db.Column(db.Date)
    pais = db.Column(db.String(50))
    salgado_favorito = db.Column(db.String(50))
    genero = db.Column(db.String(10))

with app.app_context():
    db.create_all()


# ROTAS

@app.route('/user/', methods=['POST'])
def create_user():
    data = request.form
    data_nascimento = datetime.strptime(data['data_nascimento'], '%Y-%m-%d').date()
    user = User(nome=data['nome'], email=data['email'], telefone=data['telefone'], senha=data['senha'], data_nascimento=data_nascimento, pais=data['pais'], salgado_favorito=data['salgado_favorito'], genero=data['genero'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'Usuário criado com sucesso!'}), 201




@app.route('/user/<id>', methods=['GET'])
def retrieve_user(id):
    user = User.query.get(id)
    if user is None:
        return jsonify({'message': 'Usuário não encontrado'}), 404
    else:
        return jsonify({'nome': user.nome, 'email': user.email, 'telefone': user.telefone, 'senha': user.senha, 'data_nascimento': user.data_nascimento, 'pais': user.pais, 'salgado_favorito': user.salgado_favorito, 'genero': user.genero})

@app.route('/user/<id>', methods=['PUT'])
def update_user(id):
    data = request.get_json()
    user = User.query.get(id)
    if user is None:
        return jsonify({'message': 'Usuário não encontrado'}), 404
    else:
        user.nome = data['nome']
        user.email = data['email']
        user.telefone = data['telefone']
        user.senha = data['senha']
        user.data_nascimento = data['data_nascimento']
        user.pais = data['pais']
        user.salgado_favorito = data['salgado_favorito']
        user.genero = data['genero']
        db.session.commit()
        return jsonify({'message': 'Usuário atualizado com sucesso!'})

@app.route('/user/<id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if user is None:
        return jsonify({'message': 'Usuário não encontrado'}), 404
    else:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'Usuário excluído com sucesso!'})

if __name__ == '__main__':
    app.run(debug=True)