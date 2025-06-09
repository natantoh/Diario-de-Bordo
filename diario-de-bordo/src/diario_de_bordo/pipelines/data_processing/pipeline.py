from kedro.pipeline import Pipeline, node, pipeline  # Importa classes e funções para criar pipelines e nodes no Kedro

from .nodes import (
    preprocess_companies,                            # Importa a função preprocess_companies do módulo nodes
)

def create_pipeline(**kwargs) -> Pipeline:           # Define uma função que cria e retorna um pipeline Kedro
    return pipeline(
        [
            node(
                func=preprocess_companies,          # Função que será executada neste node
                inputs="companies",                 # Nome do dataset de entrada (do Data Catalog)
                outputs="preprocessed_companies",   # Nome do dataset de saída (será salvo no Data Catalog)
                name="preprocess_companies_node",   # Nome identificador do node no pipeline
            ),
        ]
    )
