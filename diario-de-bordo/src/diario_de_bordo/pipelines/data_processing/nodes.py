
########
#### AQUI TEM TODAS AS FUNÇÕES PYTHON ( NODES )
#######

from pyspark.sql import DataFrame as SparkDataFrame
from pyspark.sql import functions as f
from pyspark.sql import SparkSession
from pyspark.sql.types import DoubleType, LongType

def processar_info_corridas_do_dia(df: SparkDataFrame) -> SparkDataFrame:

    """
    Recebe um dataframe, processa e salva uma tabela Delta agrupada por dia, a tabela final é particionada por DT_REFE.
    """

    df.show()
    df.printSchema()

    df = ( df.distinct()
            .select(

                f.date_format(f.to_timestamp("DATA_INICIO", "MM-dd-yyyy HH:mm"), "yyyy-MM-dd").alias("DT_REFE"),
                f.col("DISTANCIA").cast(DoubleType()).alias("DISTANCIA"),
                f.when( 
                        f.col("CATEGORIA") == "Negocio", 1 
                    ).otherwise(0).alias("IN_NEGOCIO"),

                f.when(f.col("CATEGORIA") == "Pessoal", 1
                    ).otherwise(0).alias("IN_PESSOAL"),

                f.when(
                        f.col("PROPOSITO") == "Reunião", 1
                    ).otherwise(0).alias("IN_REUNIAO"),

                f.when(
                    (f.col("PROPOSITO").isNotNull()) &
                    (f.trim(f.col("PROPOSITO")) != "") &
                    (f.col("PROPOSITO") != "Reunião"),
                    1
                ).otherwise(0).alias("IN_NAO_REUNIAO")

            )
        )

    df.show()
    df.printSchema()

    # Agregações
    result = (
        df.groupBy("DT_REFE")
        .agg(
            f.count("*").cast(LongType()).alias("QT_CORR"),
            f.sum("IN_NEGOCIO").cast(LongType()).alias("QT_CORR_NEG"),
            f.sum("IN_PESSOAL").cast(LongType()).alias("QT_CORR_PESS"),
            f.max("DISTANCIA").alias("VL_MAX_DIST"),
            f.min("DISTANCIA").alias("VL_MIN_DIST"),
            f.round( f.avg("DISTANCIA"), 2).alias("VL_AVG_DIST"),
            f.sum("IN_REUNIAO").cast(LongType()).alias("QT_CORR_REUNI"),
            f.sum("IN_NAO_REUNIAO").cast(LongType()).alias("QT_CORR_NAO_REUNI"),
        )
    )

    result.show()
    result.printSchema()

    return result