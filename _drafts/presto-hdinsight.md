---
published: false
---
## Presto on HDInsight

How to run Presto on HDInsight
If you are faimilier with presto and want to 

WASB support.

Presto logo + HDInsight logo


# What is Presto?
Presto is a distributed SQL query engine for big data.
Its known for being fast

It supports querying data in wide range of format including Parquet, ORC, Text, RCFile and so on.
The presto 

# Presto Architecture
To understand how does presto works, lets looks at the presto architecture. The below figures are taken from presto website and facebook presentations.

![presto-overview.png]({{site.baseurl}}/images/presto-overview.png)


The following figure from the presto documentation highlights key componenets of presto.

![presto-arch.png]({{site.baseurl}}/images/presto-arch.png)

Presto has coordinator and workers

https://github.com/prestodb/presto/blob/master/presto-docs/src/main/sphinx/overview/concepts.rst

Workers and coordinator talks via REST API. 

Federated query model that presto uses 

The Data source model
Presto connector architecutre, 
Each connector implements two APIs 
1. Metadata API
2. Data streaming API

![presto-internals.png]({{site.baseurl}}/images/presto-internals.png)

For further information, presto documentation is a great palce to look.

Found an issue in Preto on HDInsight, feel free to open a issue on the repo. Note that like any other custom action scripts, this is not a Microsoft Supported product.

# Currently avilable connectors

Some of the [connectors](https://prestodb.io/docs/current/connector.html) include 
- [Kafka](https://prestodb.io/docs/current/connector/kafka.html), 
- [Cassandra](https://prestodb.io/docs/current/connector/cassandra.html), 
- [Hive](https://prestodb.io/docs/current/connector/hive.html), 
- [Accumulo](https://prestodb.io/docs/current/connector/accumulo.html), 
- [MongoDB](https://prestodb.io/docs/current/connector/mongodb.html), 
- [MySQL](https://prestodb.io/docs/current/connector/mysql.html), 
- [PostegreSQL](https://prestodb.io/docs/current/connector/postgresql.html), 
- [Redis](https://prestodb.io/docs/current/connector/redis.html)
- ... [more](https://prestodb.io/docs/current/connector.html).

The HDInsight script only confgiures hive and [TPCH](https://prestodb.io/docs/current/connector/tpch.html) connetors by default. If you want to add other conenctors, following the instructions below.

# Use cases
While presto is very successfully used by nuber of orgnizations for their fast data anlysis needs,
One of the prime aspect that caught my attention was the ability to query various data sources in a single query. This is so magical ✨, let me give you an example,

This allows querying data without the need to bring all the data in the same place. This also obviates the need to bring all the data manged under the same system. This in my opinion is so important since, the world where each system wants to be the _only_ system to store and process data, presto does not. For real-world usecases each system has different tradeoffs and are fit and serve only part of the larger picture in teh big data architectures.

Presto supprts wide range of [inbuilt and user defined functions](https://prestodb.io/docs/current/functions.html)

The SQL syntax is similar to Hive and Spark SQL syntax and should make you feel home. It even has a [migration guide from Hive](https://prestodb.io/docs/current/migration/from-hive.html) :) Also the auto-complete in presto CLI is pretty dope!.

# Presto UI
![prestoui.png]({{site.baseurl}}/images/prestoui.png)


# Airpal
[Airpal](http://airbnb.io/airpal/) is the web query interface for presto. The following GIF from the airpal website gives good overview of available features.

![airpla-demo.gif]({{site.baseurl}}/images/airpla-demo.gif)


## Installing airpal on headnode
Install the presto by following the steps. Now, SSH to the headnode an run the [install airpal](https://github.com/dharmeshkakadia/presto-hdinsight/blob/master/installairpal.sh) script as sudo as follows.
``
cd /var/lib/presto/
sudo ./presto-hdinsight-master/installpresto.sh
``

## Installing airpal on Edgenode
You can install Airpal in HDInsight on an Edge node using [airpal-deploy.json](https://github.com/dharmeshkakadia/presto-hdinsight/blob/master/airpal-deploy.json). The step by step by instruction is listed in the [README](https://github.com/dharmeshkakadia/presto-hdinsight#airpal)

Note that with little work, you can combine both the installation with a single azure deployment template.

JDBC/ODBC drivers are available which allow you to connect to wide range of tools for querying. Ofcourse Presto has [client libraries in wide range of lanugauges](https://prestodb.io/docs/current/admin/tuning.html) if you prefer.

# Who is using Presto?
Presto started out at Facebook and has gained a lot of momentum at many organizations. Some of the promiment names are 
- Netflix
- Airbnb
- Dropbox
- LinkedIn
- Uber
- NASDAQ
- Walmart
- Alibaba
- ... [many more](https://github.com/prestodb/presto/wiki/Presto-Users) and may be YOU :)


# Step by Step instructions

Presto on HDInsight is supported using [custom action scripts](https://docs.microsoft.com/en-us/azure/hdinsight/hdinsight-hadoop-customize-cluster-linux). [Presto custom action script](https://github.com/dharmeshkakadia/presto-hdinsight) can be used on new and existing 3.5+ Hdinsight hadoop clusters to install and run presto. There is essentially only one step : to run script action with following URL on headnodes and workernodes.

``
https://raw.githubusercontent.com/dharmeshkakadia/presto-hdinsight/master/installpresto.sh
``

The below GIF shows the step while creating the clsuter.

![presto-install-steps.gif]({{site.baseurl}}/images/presto-install-steps.gif)

# Inner working of installation script
If you are interestred in the details of what is the above script doing, let me break it down.

[installpresto.sh](https://github.com/dharmeshkakadia/presto-hdinsight/blob/master/installpresto.sh) is the script invoked by custome script action. It does mainly the following things:

We use [Slider](https://github.com/prestodb/presto-yarn) to manage presto resources through YARN. In a N node standalone cluster with this script means it will create N-2 containers with maximum memory, 1 slider AM that monitors any failed containers and relaunches it a presto co-ordinator.

1. Download the the github repo.
2. Create a [presto build](https://github.com/dharmeshkakadia/presto-hdinsight/blob/master/createsliderbuild.sh) that has support of Windows Azure Storage Blob (WASB). Note that this step is required since the WASB support has not [merged](https://github.com/prestodb/presto-hadoop-apache2/pull/14) in the upstream Presto yet. The script builds the package under ``/var/lib/presto/`` on the primary headnode.
3. Install the created slider package.
4. Create appropriate presto configuration files for the presto slider package. All the configs are generated by [createconfigs.sh](https://github.com/dharmeshkakadia/presto-hdinsight/blob/master/createconfigs.sh) script. 
5. Start the presto with slider.
6. Wait for the presto to come up and install [preso-cli](https://prestodb.io/docs/current/installation/cli.html) in the ``/usr/local/bin/``.

## Customizing installation 

https://github.com/dharmeshkakadia/presto-hdinsight#how-do-i-customize-presto-installation

## Connector configuration 

As mentioned earlier, by default we have hive and tpch connectors installed with the following configurations.

Also, presto by default configuration 

## JVM configuration

The 
https://prestodb.io/docs/current/admin/tuning.html


How to run presto TPCDS article link



https://prestodb.io/
