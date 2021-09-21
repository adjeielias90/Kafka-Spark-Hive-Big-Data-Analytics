# Big Data Analytics Pipeline with Twitter, Spark, Kafka and Hive

# Ubuntu, latest version

### note '~$' is not part of the commands

## Python Version and Python setup
#### Use Python 3.6.0 for your environment
Pyenv is a python environment manager. Pyenv enables you to install different python
versions and switch between thme seamlessly

Installation and setup instructions:
[Install Pyenv](https://github.com/pyenv/pyenv#installation)

## Install Kafka
Download this version(Copy/Paste into google): kafka_2.12-2.2.0.tgz

Remember to keep copies of your hadoop and kafka installations in your root folder if you intend to run the binaries from there instead of adding it to your path

```
~$ tar -xvf kafka_2.12-2.2.0.tgz
~$ mv kafka_2.12-2.2.0 kafka
```
## Install open-jdk

```
~$ sudo apt install openjdk-8-jdk -y
~$ java -version
```

## Install python3 and then pip, python3 comes bundled with the latest version of ubuntu
```
~$ sudo apt install python3-pip
```

## Confirm install success
```
~$ pip3 list | grep kafka
```

### Install some python dependencies
```
pip install pandas plotly numpy matplotlib textblob
```


## Install hadoop
### First download hadoop-2.8.5.tar.gz like kafka above
```
~$ tar -xvf hadoop-2.8.5.tar.gz
~$ mv hadoop-2.8.5 hadoop
~$ cd hadoop
~/hadoop$ pwd

```


### Hadoop Specific Configuration
### Edit ~/.bashrc and check if jdk is in the right path
```
export HADOOP_HOME=/home/elias/hadoop
export HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop
export HADOOP_HDFS_HOME=$HADOOP_HOME
export HADOOP_INSTALL=$HADOOP_HOME
export HADOOP_MAPRED_HOME=$HADOOP_HOME
export HADOOP_COMMON_HOME=$HADOOP_HOME
export HADOOP_HDFS_HOME=$HADOOP_HOME
export YARN_HOME=$HADOOP_HOME
export HADOOP_COMMON_LIB_NATIVE_DIR=$HADOOP_HOME/lib/native
export PATH=$PATH:$HADOOP_HOME/sbin:$HADOOP_HOME/bin
export HADOOP_OPTS="-Djava.library.path=$HADOOP_HOME/lib/native"
```

### Reload bash
```
~$ source ~/.bashrc
```

> Move inside hadoop_installation_folder/etc/hadoop

### Add the following to hadoop-env.sh
```
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
export HADOOP_CONF_DIR=${HADOOP_CONF_DIR:-"/home/<USER>/hadoop/etc/hadoop"}
```


### Replace the file core-site.xml with the following:
```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
    <configuration>
        <property>
            <name>fs.default.name</name>
            <value>hdfs://localhost:9000</value>
        </property>
    </configuration>
```

### Replace the file hdfs-site.xml with the following:
```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
    <configuration>
        <property>
            <name>dfs.replication</name>
            <value>1</value>
        </property>
        <property>
            <name>dfs.permission</name>
            <value>false</value>
        </property>
    </configuration>
```

## Install ssh
```
~$ sudo apt install openssh-server openssh-client -y
~$ ssh-keygen -t rsa
~$ cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
```

### To test ssh...
```
~$ ssh localhost
```

With Hadoop configured and SSH setup, we can start the Hadoop cluster and test the installation.
If none of these commands return an error, we are good to go.
```
~$ hdfs namenode -format
~$ start-dfs.sh
~$ hadoop fs -ls /
```

# Install Hive
These links seem to be working as of 17 Sep 2021, if the commands returns a 404, just install it like we did hadoop

```
~$ wget http://archive.apache.org/dist/hive/hive-2.3.5/apache-hive-2.3.5-bin.tar.gz
~$ tar -xvf apache-hive-2.3.5-bin.tar.gz
~$ mv apache-hive-2.3.5 hive
```

## Add permissions and directories to HDFS
```
~$ hadoop fs -mkdir -p /user/hive/warehouse
~$ hadoop fs -mkdir -p /tmp
~$ hadoop fs -chmod g+w /user/hive/warehouse
~$ hadoop fs -chmod g+w /tmp
```


### Inside ~/hive/conf/, create/edit hive-env.sh and add the following
```
export HADOOP_HOME=/home/<USER>/hadoop
export HADOOP_HEAPSIZE=512
export HIVE_CONF_DIR=/home/<USER>/hive/conf
```

### While still in ~/hive/conf, create/edit hive-site.xml and add the following
```
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<configuration>
    <property>
        <name>javax.jdo.option.ConnectionURL</name>
        <value>jdbc:derby:;databaseName=/home/<YOUR-USERNAME>/hive/metastore_db;create=true</value>
        <description>JDBC connect string for a JDBC metastore.</description>
    </property>
    <property>
        <name>hive.metastore.warehouse.dir</name>
        <value>/user/hive/warehouse</value>
        <description>location of default database for the warehouse</description>
    </property>
    <property>
        <name>hive.metastore.uris</name>
        <value>thrift://localhost:9083</value>
        <description>Thrift URI for the remote metastore.</description>
    </property>
    <property>
        <name>javax.jdo.option.ConnectionDriverName</name>
        <value>org.apache.derby.jdbc.EmbeddedDriver</value>
        <description>Driver class name for a JDBC metastore</description>
    </property>
    <property>
        <name>javax.jdo.PersistenceManagerFactoryClass</name>
        <value>org.datanucleus.api.jdo.JDOPersistenceManagerFactory</value>
        <description>class implementing the jdo persistence</description>
    </property>
    <property>
        <name>hive.server2.enable.doAs</name>
        <value>false</value>
    </property>
</configuration>
```

## Optional
Since Hive and Kafka are running on the same system, you'll get a warning message about some SLF4J logging file.
From your Hive home you can just rename the file

```
~/hive$ mv lib/log4j-slf4j-impl-2.6.2.jar lib/log4j-slf4j-impl-2.6.2.jar.bak
```

Now we need to create a database schema for Hive to work with using schematool
If you get any error on this command it's liekly your hive-site.xml configuration above.

```
~$ schematool -initSchema -dbType derby
```

### Check if metastore is running:
Keep it running and change to another terminal
```
~$ hive --service metastore
```

### Enter hive:
```
~$ hive
```

### While in hive, we will create the database for storing our Twitter data:

```
hive> CREATE TABLE tweets (text STRING, words INT, length INT)
    > ROW FORMAT DELIMITED FIELDS TERMINATED BY '\\|'
    > STORED AS TEXTFILE;

```


### Download from ,
[Spark Download](https://spark.apache.org/downloads.html)
Make sure you choose the option for Hadoop 2.7 or later (unless you used and earlier version).
Unpack it, rename it

### Install Spark
```
~$ tar -xvf spark-3.1.2-bin-hadoop2.7.tgz
~$ mv spark-2.4.3-bin-hadoop2.7.tgz spark
```

## NOTE
Although I have been able to run Spark before without installing Scala, we can avoid some issues by ensuring Scala is installed on our system.

```
~$ sudo apt install scala -y
```

### Test if scala was correctly installed
```
~$ scala -version
```

## Install PySpark
```
~$ pip3 install pyspark
```

### check our installation
```
~$ pip3 list | grep spark
```

### Now we need to add the Spark /bin files to the path, so open up .bashrc and add the following
```
export PATH=$PATH:/home/<USERNAME>/spark/bin
export PYSPARK_PYTHON=python3
```

By setting the PYSPARK_PYTHON variable, we can use PySpark with Python3, the version of Python we have been using so far.

### After running `source ~/.bashrc`, try entering the PySpark shell
```

~$ pyspark
```

# Running our code: 
### cd into our root folder

### We need 7 terminal windows for now


### FOR COMMANDS 1-3, 
```
~$ cd kafka
```

### Zookeeper

1. start zookeeper
```
./bin/zookeeper-server-start.sh config/zookeeper.properties

./bin/zookeeper-server-start.sh ./config/zookeeper.properties
```

### Kafka Broker

2. start kafka broker
```
./bin/kafka-server-start.sh config/server.properties
```


### Kafka Configuration

3. some kafka configuration
Check for existing topics
```
./bin/kafka-topics.sh --list --bootstrap-server localhost:9092
```

Create our tweets topic
```
./bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic tweets
```

### Hive Metastore
4. start hive metastore service
```
~$ hive --service metastore
```

### Hive Service
5. start hive service
```
~$ hive

 ...


hive> use default;
hive> select count(*) from tweets;
```

### Stream producer 
6. start the stream producer
```
~$ chmod 755 tweet_stream.py
~$ python3 tweet_stream.py
```

# Spark Consumer
7. start the spark consumer
```
~$ spark-submit --jars spark-streaming-kafka.jar files/transformer.py
```

# Exporting data from Hive warehouse in HDFS
# This has already been done in the data_analytics python file, however, if for any reason you need to
# export data from hdfs, this is the way to do it directly for hive, otherwise use spark SQL.


# NOTE that the data analytics python file needs to be started manually, and requires python 3.7.+

## Some extra commands you may need:

### Hive
```
Select text from tweets where text rlike '.*(covid).*';
hive -e INSERT OVERWRITE LOCAL DIRECTORY '/home/elias/Desktop/export' ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' SELECT text FROM tweets WHERE text rlike '.*(kabul).*';
hive -e INSERT OVERWRITE LOCAL DIRECTORY '/home/elias/Desktop/export' ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' SELECT text FROM tweets WHERE text rlike '.*(programming).*';
hive -e INSERT OVERWRITE LOCAL DIRECTORY '/home/elias/Desktop/export' ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' SELECT text FROM tweets WHERE text rlike '.*(olympics).*';
INSERT OVERWRITE LOCAL DIRECTORY '/home/elias/Desktop/export' ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' SELECT text FROM tweets WHERE text rlike '.*(data science machine learning big data).*';
```

### Communicating with HIVE with SPARKSQL
```
col_names = ['tweet']

sc = SparkContext(appName="Something")                                                                                                                                                                              
                                                                                                                        
spark = SparkSession.builder.appName("Something").config("spark.sql.warehouse.dir", "/user/hive/warehouse").config("hive.metastore.uris", "thrift://localhost:9083").enableHiveSupport().getOrCreate()      


# read our data from hive as a pandas dataframe, pass column names as columns
big_data_query = spark.sql("SELECT text FROM tweets WHERE text rlike '.*(big data).*'")
```
