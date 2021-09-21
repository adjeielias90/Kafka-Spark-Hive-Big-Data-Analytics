elias@thinkpad460:~/Desktop/project/spark-kafka-streaming$ spark-shell
Setting default log level to "WARN".
To adjust logging level use sc.setLogLevel(newLevel). For SparkR, use setLogLevel(newLevel).
21/09/19 16:03:20 WARN util.Utils: Your hostname, thinkpad460 resolves to a loopback address: 127.0.1.1; using 192.168.201.157 instead (on interface wlp4s0)
21/09/19 16:03:20 WARN util.Utils: Set SPARK_LOCAL_IP if you need to bind to another address
21/09/19 16:03:20 WARN util.NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
Spark context Web UI available at http://192.168.201.157:4040
Spark context available as 'sc' (master = local[*], app id = local-1632085401666).
Spark session available as 'spark'.
Welcome to
      ____              __
     / __/__  ___ _____/ /__
    _\ \/ _ \/ _ `/ __/  '_/
   /___/ .__/\_,_/_/ /_/\_\   version 2.2.3
      /_/
         
Using Scala version 2.11.8 (OpenJDK 64-Bit Server VM, Java 1.8.0_292)
Type in expressions to have them evaluated.
Type :help for more information.

scala> import org.apache.spark.sql.{DataFrame, SaveMode, SparkSession}
import org.apache.spark.sql.{DataFrame, SaveMode, SparkSession}

scala> val spark = SparkSession.builder().appName("Something").config("spark.sql.warehouse.dir", "/user/hive/warehouse").config("hive.metastore.uris", "thrift://localhost:9083").enableHiveSupport().getOrCreate()
21/09/19 16:03:36 WARN metastore.ObjectStore: Failed to get database global_temp, returning NoSuchObjectException
21/09/19 16:03:36 WARN sql.SparkSession$Builder: Using an existing SparkSession; some configuration may not take effect.
spark: org.apache.spark.sql.SparkSession = org.apache.spark.sql.SparkSession@723081a2

scala> val df = spark.sql("SELECT text FROM tweets");
df: org.apache.spark.sql.DataFrame = [text: string]

scala> df.show();
+--------------------+
|                text|
+--------------------+
|So much of the Tr...|
|The new issue of ...|
|French show stron...|
|          ABD ,\N,\N|
|FDA (Gıda ve İlaç...|
|2’ye karşı 16 oy ...|
|3.doz PfizerBioNT...|
|Hasty mistaken #d...|
|İBB’nin konser st...|
|‘US admits strike...|
|@MoE_TEQIPF is de...|
|oppression olympi...|
|After Kabul, now ...|
|Image of #Taliban...|
|Which IDE do you ...|
|             .,\N,\N|
|             .,\N,\N|
|            . ,\N,\N|
|#BigData #Analyti...|
|Dopo giorni di pa...|
+--------------------+
only showing top 20 rows


scala> 

