from datetime import datetime, date, time
from core.services.ConnectionService import ConnectionService

# Este método é o construtor da classe. Ele recebe uma instância de 
# ConnectionService e um nome de banco de dados (dbname). No construtor, 
# a conexão ao banco de dados MongoDB é estabelecida utilizando a instância de 
# ConnectionService, e o banco de dados específico é selecionado
class MongoService:
    def __init__(self, conection: ConnectionService, dbname) -> None:
        self.client = conection.getConnection()
        self.db = self.client[dbname]
# Este método insere um documento na coleção especificada (collection). 
# Ele recebe os dados como kwargs, converte a data 
# (se a chave for "validade" e o valor for do tipo date), e insere o documento na coleção.
    def insert(self, collection, **kwargs):
        data = {}
        collection = self.db[collection]
        for key, value in kwargs.items():
            if key == "validade" and isinstance(value, date):
                value = datetime.combine(value, time())
            data[key] = value
        collection.insert_one(data)
# Esses métodos realizam operações de consulta na coleção especificada. O método find retorna um 
# cursor para os documentos que correspondem aos critérios dados, findOne retorna um único documento
# que corresponde aos critérios e findAll retorna todos os documentos que correspondem aos critérios.
    def find(self, collection, **kwargs):
        collection = self.db[collection]
        return collection.find(kwargs)

    def findOne(self, collection, **kwargs):
        collection = self.db[collection]
        return collection.find_one(kwargs)

    # findAll
    def findAll(self, collection, **kwargs):
        collection = self.db[collection]
        return collection.find(kwargs)
# Este método exclui um único documento na coleção com base na consulta fornecida (filter_query).
    def delete(self, collection, filter_query):
        collection = self.db[collection]
        collection.delete_one(filter_query)
# Este método atualiza um único documento na coleção com base na consulta (filter_query) e nos 
# dados de atualização fornecidos (update_data).
    def update(self, collection, filter_query, update_data):
        collection = self.db[collection]
        collection.update_one(filter_query, {"$set": update_data})
# Este método conta o número total de documentos na coleção que correspondem aos critérios dados (kwargs).
    # index_with_total
    def index_with_total(self, collection, **kwargs):
        collection = self.db[collection]
        return collection.find(kwargs).count()
