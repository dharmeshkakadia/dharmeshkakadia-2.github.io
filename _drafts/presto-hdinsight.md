---
layout: post
title: Presto on HDInsight
published: true
---
This article will explain presto internals and how to install presto on [Azure HDInsight](https://azure.microsoft.com/en-us/services/hdinsight/). If you are familiar with presto, you can [jump in directly](#installing-presto-on-hdinsight).

# What is Presto?
[Presto](https://prestodb.io/) is a **fast** distributed SQL query engine for big data. Presto is suitable for interactive querying of petabytes of data.

# Who is using Presto?
Presto started out at Facebook and has become key piece in the data infrastructure of many organizations. Some of the prominent names who use presto are:
- Netflix
- Airbnb
- Dropbox
- LinkedIn
- Uber
- NASDAQ
- Walmart
- Alibaba
- ... [many more](https://github.com/prestodb/presto/wiki/Presto-Users) and may be, by the end of this article, YOU :)

# Presto Architecture
To understand how presto works, lets look at the presto architecture. The following figure from the presto documentation highlights key [components](https://github.com/prestodb/presto/blob/master/presto-docs/src/main/sphinx/overview/concepts.rst) of presto.

![presto-arch.png]({{site.baseurl}}/images/presto-arch.png)

## Clients
Clients are where you submit queries to Presto. Clients can use JDBC/ODBC/REST protocol to talk to coordinator.

## Coordinator
Presto coordinator is responsible for managing workernode membership, parsing the queries, generating execution plan and managing execution of the query. During the execution of the queries, it also manages the delivery of the data between tasks.

The coordinator translates the given query into logical plan. The logical plan is composed of seires of stages and each stage is then executed in a disstributed fashion using several tasks across workers. This is very similar to other distributed query execution engines like Hive and Spark.

## Workers
Presto worker is responsible for executing tasks and processing data. This is where the real work of processing the data happens.

## Communication
Each presto worker advertises itself to the coordinator through [discovery server](https://github.com/airlift/discovery). All the communication in presto between Coordinator, workers and clients happen via REST API.

## Connectors
Presot has a federated query model where each data sources is a presto connector. One way to think about different presto connectors is similar to how different drivers enable a database to talk to multiple sources. Some of the currently available connectors on the presto project:

- [Kafka](https://prestodb.io/docs/current/connector/kafka.html),
- [Cassandra](https://prestodb.io/docs/current/connector/cassandra.html),
- [Hive](https://prestodb.io/docs/current/connector/hive.html),
- [Accumulo](https://prestodb.io/docs/current/connector/accumulo.html),
- [MongoDB](https://prestodb.io/docs/current/connector/mongodb.html),
- [MySQL](https://prestodb.io/docs/current/connector/mysql.html),
- [PostegreSQL](https://prestodb.io/docs/current/connector/postgresql.html),
- [Redis](https://prestodb.io/docs/current/connector/redis.html)
- ... [more](https://prestodb.io/docs/current/connector.html).


## Catalog
Each catalog in presto is associated with a specific connector, specified in the catalog configuration with ``connector.name``. Based on this name Presto (Catalog Manager) decides how to query a perticular data source. When writing a query in Presto, you can use the fully-qualified name that contains ``connector.schemaname.tablename``. For example, if you have a hive table ``revenue`` in database name ``prod``, you can refer it as ``hive.prod.revenue``. The below figure highlights how multiple catalogs fit in presto:

![presto-internals.png]({{site.baseurl}}/images/presto-internals.png)

As showed in the figure, each connector implements two APIs
1. Data streaming API : Specifies how to read/write the data.
2. Metadata API : Specifies what is the schema or how to interpret the data.

For further information, [presto documentation](https://prestodb.io/docs/current) is a great place to look :)

# Presto Use Cases
Presto is suitable for interactive query 
While presto is very successfully used by number of organizations for their fast data analysis needs,
One of the prime aspect that caught my attention was the ability to query various data sources in a single query. This is so magical ✨, let me give you an example,

```sql
SELECT s.region, 
       revenue 
FROM   hive.weblog.clickstreams s 
       JOIN mysql.prod.transections t 
         ON s.userid = t.userid 
GROUP  BY s.region 
ORDER  BY revenue DESC 
LIMIT  100
```

This allows querying data without the need to bring all the data in the same place. This also obviates the need to bring all the data managed under the same system. This in my opinion is so important since, the world where each system wants to be the _only_ system to store and process data, presto does not. For real-world usecases each system has different tradeoffs and are fit and serve only part of the larger picture in the big data architectures.

Presto supprts wide range of [inbuilt and user defined functions](https://prestodb.io/docs/current/functions.html)

The SQL syntax is similar to Hive and Spark SQL syntax and should make you feel home. It even has a [migration guide from Hive](https://prestodb.io/docs/current/migration/from-hive.html) :) Also the auto-complete in presto CLI is pretty dope!.

# Presto UI
![prestoui.png]({{site.baseurl}}/images/prestoui.png)


# Airpal
[Airpal](http://airbnb.io/airpal/) is the web query interface for presto. The following GIF from the airpal website gives good overview of available features.

![airpla-demo.gif]({{site.baseurl}}/images/airpla-demo.gif)


## Installing airpal on headnode
Install the presto by following the steps. Now, SSH to the headnode and tun the following command to figure out 

an run the [install airpal](https://github.com/dharmeshkakadia/presto-hdinsight/blob/master/installairpal.sh) script as sudo as follows.
``
cd /var/lib/presto/
sudo ./presto-hdinsight-master/installpresto.sh
``

The airpal will be running on port 9191.

## Installing airpal on Edgenode
You can install Airpal in HDInsight on an Edge node using [airpal-deploy.json](https://github.com/dharmeshkakadia/presto-hdinsight/blob/master/airpal-deploy.json). The step by step by instruction is listed in the [README](https://github.com/dharmeshkakadia/presto-hdinsight#airpal)

While 

Note that with little work, you can combine both the installation with a single azure deployment template.

JDBC/ODBC drivers are available which allow you to connect to wide range of tools for querying. Ofcourse Presto has [client libraries in wide range of lanugauges](https://prestodb.io/docs/current/admin/tuning.html) if you prefer.


# Installing Presto on HDInsight

Presto on HDInsight is supported using [custom action scripts](https://docs.microsoft.com/en-us/azure/hdinsight/hdinsight-hadoop-customize-cluster-linux). [Presto custom action script](https://github.com/dharmeshkakadia/presto-hdinsight) can be used on new and existing 3.5+ HdInsight hadoop clusters to install and run presto. There is essentially only one step : to run script action with following URL on headnodes and workernodes.

``
https://raw.githubusercontent.com/dharmeshkakadia/presto-hdinsight/master/installpresto.sh
``

The below GIF shows the step while creating the cluster.

![presto-install-steps.gif]({{site.baseurl}}/images/presto-install-steps.gif)

Now you can SSH to the cluster and start using it.

```
presto --schema default
```

This will drop you into presto-cli and you can start analyzing data right away.

```
presto> select count(*) from hivesampletable;
```

You can also run TPCH or [TPCDS](https://github.com/dharmeshkakadia/presto-hdinsight#how-do-i-run-tpcds-on-presto).

If you find any issues in Presto on HDInsight, feel free to open a [issue](https://github.com/dharmeshkakadia/presto-hdinsight/issues/new). Note that like any other custom action scripts, this is not a Microsoft Supported product.

# Inner working of installation script
If you are interestred in the details of what is the above script doing, let me break it down.

[installpresto.sh](https://github.com/dharmeshkakadia/presto-hdinsight/blob/master/installpresto.sh) is the script invoked by custom script action. It performs the following steps:

We use [Slider](https://github.com/prestodb/presto-yarn) to manage presto resources through YARN. In a N node standalone cluster with this script means it will create N-2 containers with maximum memory, 1 slider AM that monitors any failed containers and relaunches it a presto co-ordinator.

1. Download the github repo.
2. Create a [presto build](https://github.com/dharmeshkakadia/presto-hdinsight/blob/master/createsliderbuild.sh) that has support of Windows Azure Storage Blob (WASB). Note that this step is required since the WASB support has not [merged](https://github.com/prestodb/presto-hadoop-apache2/pull/14) in the upstream Presto yet. The script builds the package under ``/var/lib/presto/`` on the primary headnode.
3. Install the created slider package.
4. Create appropriate presto-slider configuration files (``appConfig-default.json`` and ``resources-default.json``) for the presto slider package. All the configs are generated by [createconfigs.sh](https://github.com/dharmeshkakadia/presto-hdinsight/blob/master/createconfigs.sh) script. This configure Hive and TPCH connectors. Hive connector is configured to use the default installed Hive installation, so all the tables from Hive will be automatically visible with presto.
5. Start the presto with slider.
6. Wait for the presto to come up and install [preso-cli](https://prestodb.io/docs/current/installation/cli.html) in the ``/usr/local/bin/``.

## Customizing installation

Folllow the steps mentioned in [How do I customize presto installation](https://github.com/dharmeshkakadia/presto-hdinsight#how-do-i-customize-presto-installation).
