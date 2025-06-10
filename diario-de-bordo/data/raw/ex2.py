from pyspark.sql import SparkSession

### CÓDIGO SÓ PARA LER A TABELA DELTA CRIADA NO PIPELINE
spark = (
    SparkSession.builder
    .appName("DeltaRead")
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
    .config("spark.jars.packages", "io.delta:delta-core_2.12:2.4.0")
    .getOrCreate()
)

delta_path = "diario-de-bordo/data/processed/info_corridas_do_dia"
df = spark.read.format("delta").load(delta_path)
df.show()