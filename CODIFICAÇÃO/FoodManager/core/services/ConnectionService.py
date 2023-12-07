import pymongo

#instanciacao de uma classe e getconnection cria uma coneccao e retorna uma conexao com o banco mongodb
class ConnectionService:
    def getConnection(self):
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        return client
