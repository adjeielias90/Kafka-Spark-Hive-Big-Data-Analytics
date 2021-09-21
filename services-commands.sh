#!/bin/sh
#before you start the script, run:
# chmod a+x services-commands.sh

# run script with ./services-commands.sh

# MAKE SURE THIS SCRIPT IS IN THE ROOT FOLDER OF THE PROJECT 


# move to kafka
cd kafka

# 1: start zookeeper
gnome-terminal -e "bash -c './bin/zookeeper-server-start.sh ./config/zookeeper.properties'"
# ./bin/zookeeper-server-start.sh ./config/zookeeper.properties

# 2: start kafka broker
gnome-terminal -e "bash -c './bin/kafka-server-start.sh config/server.properties'"
# ./bin/kafka-server-start.sh config/server.properties

# create our tweets topic
# if this script fails remember to delete the topic or you'll get an error
gnome-terminal -e "bash -c './bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic tweets
'"
# ./bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic tweets


# kafka job done, moving out.
cd ..
cd files

# start application
chmod 755 tweet_stream.py
python3 tweet_stream.py

# start hive metastore service
# NOTE: this command assumes you have hive installed and add to $PATH on windows and ~/.basrc on linux/unix
# for instructions on how to do this perform a google search or look in the environment_setup.md file
hive --service metastorehive --service metastore



