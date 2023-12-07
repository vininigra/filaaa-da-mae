from .repositories.FoodManagerRepository import FoodManagerRepository
from bson import ObjectId


class CadastroProdutoService:
# O construtor recebe uma instância de FoodManagerRepository como parâmetro 
# e a armazena em um atributo chamado repository
    def __init__(self, repository: FoodManagerRepository) -> None:
        self.repository = repository
# Este método chama o método insert da instância de FoodManagerRepository, inserindo um documento
# na coleção "Produtos" com os dados fornecidos
    def insert(self, data):
        return self.repository.insert("Produtos", **data)


class CadastroRequerenteService:
# O construtor recebe uma instância de FoodManagerRepository como parâmetro e a armazena
# em um atributo chamado repository.
    def __init__(self, repository: FoodManagerRepository) -> None:
        self.repository = repository
# Este método chama o método insert,updata,delete da instância de FoodManagerRepository, inserindo um 
# documento na coleção "Requerentes" com os dados fornecidos
    def insert(self, data):
        return self.repository.insert("Requerentes", **data)

    def update(self, data):
        return self.repository.update("Requerentes", **data)

    def delete(self, data):
        return self.repository.delete("Requerentes", **data)


class DoacaoService:
# O construtor recebe uma instância de FoodManagerRepository como parâmetro e a armazena em
# um atributo chamado repository.
    def __init__(self, repository: FoodManagerRepository) -> None:
        self.repository = repository
# Converte o alimento_id para um objeto ObjectId.
# Exclui um documento da coleção "Produtos" usando o delete_one.
# Atualiza documentos na coleção "Relatorio" removendo o item da lista "produtos" com base no alimento_id.
    def delete(self, alimento_id):
        alimento_id = ObjectId(alimento_id)
        condicao = {"_id": alimento_id}
        produtos_collection = self.repository.get_collection("Produtos")
        produtos_collection.delete_one(condicao)
        # produtos.delete({"_id": alimento_id})
        update_query = {"$pull": {"produtos": {"_id": alimento_id}}}

        self.repository.update("Relatorio", condicao=condicao, **update_query)
