from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, DoubleType

# Cria uma sessão Spark local para teste
spark = SparkSession.builder \
    .appName("MockTest") \
    .master("local[*]") \
    .getOrCreate()

def mock_df_para_processar_info_corridas_do_dia(spark: SparkSession):

    """Cria e retorna o DataFrame simulado para o node processar_info_corridas_do_dia"""
    
    schema = StructType([
        StructField("DATA_INICIO", StringType(), True),
        StructField("DATA_FIM", StringType(), True),
        StructField("CATEGORIA", StringType(), True),
        StructField("LOCAL_INICIO", StringType(), True),
        StructField("LOCAL_FIM", StringType(), True),
        StructField("DISTANCIA", DoubleType(), True),
        StructField("PROPOSITO", StringType(), True)
    ])

    data = [
        {
            "DATA_INICIO": "01-05-2016 17:31",
            "DATA_FIM": "01-05-2016 17:45",
            "CATEGORIA": "Negocio",
            "LOCAL_INICIO": "Fort Pierce",
            "LOCAL_FIM": "West Palm Beach",
            "DISTANCIA": 10.5,
            "PROPOSITO": "Reunião"
        },
        {
            "DATA_INICIO": "02-05-2016 10:12",
            "DATA_FIM": "02-05-2016 10:40",
            "CATEGORIA": "Pessoal",
            "LOCAL_INICIO": "Miami",
            "LOCAL_FIM": "Orlando",
            "DISTANCIA": 32.0,
            "PROPOSITO": "Lazer"
        }
    ]

    return spark.createDataFrame(data, schema=schema)