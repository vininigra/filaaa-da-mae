# Importe a função no início do seu arquivo (se ainda não estiver importada)
from views import get_total_products

# ...

# Em algum lugar do seu código, chame a função e imprima o resultado
total_produtos = get_total_products()
print(f'Total de Produtos: {total_produtos}')
