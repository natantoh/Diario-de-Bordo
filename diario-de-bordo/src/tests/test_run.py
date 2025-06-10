import pytest
from pyspark.sql import SparkSession
from diario_de_bordo.pipelines.data_processing.nodes import processar_info_corridas_do_dia
from tests.utils.moc_data import mock_df_para_processar_info_corridas_do_dia

# Setup SparkSession para testes
@pytest.fixture(scope="session")
def spark():
    return SparkSession.builder \
        .appName("TestSession") \
        .master("local[2]") \
        .getOrCreate()

@pytest.mark.unit
def test_processar_info_corridas_do_dia(spark):
    # Usa função mock específica para este node
    input_df = mock_df_para_processar_info_corridas_do_dia(spark)

    # Define as colunas esperadas do resultado
    expected_columns = {
        "DT_REFE", "QT_CORR", "QT_CORR_NEG", "QT_CORR_PESS",
        "VL_MAX_DIST", "VL_MIN_DIST", "VL_AVG_DIST",
        "QT_CORR_REUNI", "QT_CORR_NAO_REUNI"
    }

    # Executa o node e realiza validações
    result_df = processar_info_corridas_do_dia(input_df)
    result_columns = set(result_df.columns)

    assert expected_columns.issubset(result_columns)
    assert result_df.count() == 2
