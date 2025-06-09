
########
#### AQUI TEM TODAS AS FUNÇÕES PYTHON ( NODES )
#######

import pandas as pd
from pyspark.sql import Column
from pyspark.sql import DataFrame as SparkDataFrame
from pyspark.sql.functions import regexp_replace
from pyspark.sql.types import DoubleType

def _is_true(x: Column) -> Column:
    return x == "t"

def _parse_percentage(x: Column) -> Column:
    x = regexp_replace(x, "%", "")
    x = x.cast("float") / 100
    return x

def preprocess_companies(companies: SparkDataFrame) -> tuple[SparkDataFrame, dict]:
    """Preprocesses the data for companies.

    Args:
        companies: Raw data.
    Returns:
        Preprocessed data, with `company_rating` converted to a float and
        `iata_approved` converted to boolean.
    """


    import pyspark
    print(pyspark.__version__)

    from pyspark.sql import SparkSession
    spark = SparkSession.builder.getOrCreate()
    print(f"versão do spark: {spark.version}")

    companies = companies.withColumn("iata_approved", _is_true(companies.iata_approved))
    companies = companies.withColumn("company_rating", _parse_percentage(companies.company_rating))

    # Drop columns that aren't used for model training
    companies = companies.drop('company_location', 'total_fleet_count')
    return companies
