from flask import Flask,jsonify, request
import uuid
app = Flask(__name__)
entidades = [
]
def create_app():
    @app.route('/entidades', methods = ['GET'])
    def obter_entidades():
        return jsonify(entidades)

    @app.route('/entidades/<string:cnpj>',methods=['GET'])
    def obter_entidades_por_cnpj(cnpj):
        for entidade in entidades:
            if entidade['CNPJ'] == cnpj:
                return jsonify(entidade)


    @app.route('/entidades/usuarios/<string:cnpj>',methods=['POST','GET'])
    def add_usuarios(cnpj):

        if request.data:
            usuario = request.get_json()
            unique_id = uuid.uuid5(uuid.NAMESPACE_DNS,str(usuario))
            dados = {"codigo":str(unique_id)}
            dados.update(usuario)
        for indice,entidade in enumerate(entidades):
            if entidade['CNPJ'] == cnpj:
                if request.data:
                    entidades[indice]["usuarios"].append(dados)
                return jsonify(entidades)
            else:
                return "CNPJ Não encontrado"


    @app.route('/entidades', methods = ['POST'])
    def nova_entidade():
        nova_entidade = request.get_json()
        entidades.append(nova_entidade)

        return jsonify(entidades)

    @app.route('/login')
    def login():
        user = request.args.get('user')
        senha = request.args.get('password')

        for entidade in entidades:
            for usuario in entidade['usuarios']:
                if usuario['usuario'] == user and usuario['senha'] == senha:
                    return jsonify(usuario)
                else:
                    return "nenhum usuário encontrado"
    return app