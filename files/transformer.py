from pyspark import SparkContext                                                                                    
from pyspark.sql import SparkSession                                                                          
from pyspark.streaming import StreamingContext                            
from pyspark.streaming.kafka import KafkaUtils
                                                                         
                                                                                                                        
def handle_rdd(rdd):                                                                                        
    if not rdd.isEmpty():                                                                                               
        global ss                                                                                                    
        df = ss.createDataFrame(rdd, schema=['text', 'words', 'length'])                                       
        df.show()                                       
        df.write.saveAsTable(name='default.tweets', format='hive', mode='append')                     

                                                                   
sc = SparkContext(appName="Something")                                                                                     
ssc = StreamingContext(sc, 5)                                                                                           
                                                                                                                        
ss = SparkSession.builder.appName("Something").config("spark.sql.warehouse.dir", "/user/hive/warehouse").config("hive.metastore.uris", "thrift://localhost:9083").enableHiveSupport().getOrCreate()      


ss.sparkContext.setLogLevel('WARN')                                                                          
ks = KafkaUtils.createDirectStream(ssc, ['tweets'], {'metadata.broker.list': 'localhost:9092'})                       
                                                                                                                        
lines = ks.map(lambda x: x[1])                                                                      
                                                                                                                        
transform = lines.map(lambda tweet: (tweet, int(len(tweet.split())), int(len(tweet))))     
                                                                                                                        
transform.foreachRDD(handle_rdd)                                                                                        
                                                                                                                        
ssc.start()                                                                                                             
ssc.awaitTermination()

'''
    In our spark consumer we create a spark context using the pyspark module.
    We then create a streaming context and pass our spark context and time interval where our streaming data will be divided into batches
    We are doing real-time batch processing after all.
    We then initailize a spark session with the configuration of the location of our hive warehouse, to tell spark where to save our data
    and spark sql configuration also to tell spark how to wirte our data. We also enable hive support here to enable our spark session to
    be able to connect to hive.

    We also import a Kafka Utils library to create a direct stream from the port 9092 where our Kafka producer keeps our incoming data from twitter
    Finally, we transform this data and create an RDD from it and save it to our hive datastore so we can retireve it later to perform further analysis.
    
'''