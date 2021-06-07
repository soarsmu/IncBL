#!/bin/bash
echo "create directory to store codebase"
mkdir /home/jack/codebase
cd /home/jack/codebase
echo "Downloading codebase for Bugzbook..."
# git clone https://github.com/apache/ambari.git
# git clone https://github.com/apache/bigtop.git
# git clone https://github.com/apache/camel.git
# git clone https://github.com/apache/cassandra.git
# git clone https://github.com/apache/cxf.git
# git clone https://github.com/apache/drill.git
# git clone https://github.com/apache/hbase.git
# git clone https://github.com/apache/hive.git
# git clone https://github.com/apache/jackrabbit.git
# git clone https://github.com/apache/karaf.git
# git clone https://github.com/apache/commons-lang.git
# git clone https://github.com/apache/mahout.git
# git clone https://github.com/apache/commons-math.git
# git clone https://github.com/opencv/opencv.git
# git clone https://github.com/apache/opennlp.git
# git clone https://github.com/pandas-dev/pandas.git
# git clone https://github.com/apache/pdfbox.git
# git clone https://github.com/apache/pig.git
# git clone https://github.com/apache/solr.git
# git clone https://github.com/apache/spark.git
# git clone https://github.com/apache/sqoop.git
# git clone https://github.com/tensorflow/tensorflow.git
# git clone https://github.com/apache/tez.git
# git clone https://github.com/apache/tika.git
# git clone https://github.com/apache/wicket.git
# git clone https://github.com/apache/struts.git
# git clone https://github.com/apache/zookeeper.git

cd /home/jack/spilted_bugz
for folder in `ls $1`
do
    while read -r line
    do
        cd /home/jack/codebase/$folder
        ver=$(git rev-list --all -n 1 --before="$line|cut -d | -f 2")
        git reset --hard $ver
        cd /home/jack/spilted_bugz/$folder
        bug=$(echo $line|cut -d "L" -f 1)
        python "/home/jack/Blinpy-app/local.py" "/home/jack/Blinpy-app" "/home/jack/spilted_bugz/$folder/$bug""L" "/home/jack/codebase/$folder"
    done < /home/jack/spilted_bugz/$folder"/""id_time.txt"
done
