from core.services.ConnectionService import ConnectionService


class FoodManagerRepository:
#metodo construtor instancia a conexao com o banco de dados pelo connectionservice
# e os outros parametros são passados para o construtor da classe ConnectionService
    def __init__(self, conexao: ConnectionService) -> None:
        self.conexao = conexao

    def insert(self, collection, **kwargs):
        self.conexao.insert(collection, **kwargs)

    def find(self, collection, **kwargs):
        return self.conexao.find(collection, **kwargs)

    def update(self, collection, **kwargs):
        self.conexao.update(collection, **kwargs)

    def delete(self, collection, filter_query):
        self.conexao.delete(collection, filter_query)
