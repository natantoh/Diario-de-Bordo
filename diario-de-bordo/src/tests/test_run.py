import pytest
from kedro.framework.context import KedroContext
from kedro.framework.hooks import _create_hook_manager
from kedro.framework.project import configure_project
from pathlib import Path

@pytest.mark.integration
def test_pipeline_runs(monkeypatch):
    """
    Testa se o pipeline principal roda sem erros e gera a tabela Delta de saída.
    """
    # Configura o projeto Kedro
    project_path = Path(__file__).resolve().parents[2]
    configure_project(project_path.name)

    # Cria o contexto do Kedro
    from kedro.framework.context import load_context
    context = load_context(project_path)

    # Executa o pipeline principal
    result = context.run()

    # Verifica se o dataset de saída foi criado no catalog
    assert "output_info_corridas_do_dia" in context.catalog.list()
    ds = context.catalog.load("output_info_corridas_do_dia")
    # Verifica se o DataFrame não está vazio
    assert ds.count() > 0