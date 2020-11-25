---
layout: post
title: Analyzing Azure Storage Performance
---
I work on performance of Big data systems at [Azure HDInsight](https://azure.microsoft.com/en-us/services/hdinsight/) and as part of [benchmarking](https://azure.microsoft.com/en-us/blog/hdinsight-interactive-query-performance-benchmarks-and-integration-with-power-bi-direct-query/), many times I need to analyze the performance of the cloud storage. Performance of the storage system plays a very critical role in the performance of the cloud big data systems. Even though there are public benchmarks available for theses systems, its important to measure performance for your workload. In that spirit, we will see how to leverage storage logs for benchmarking your big data workload on [Azure Storage Blob (aka WASB)](https://azure.microsoft.com/en-us/services/storage/). We will see how to enable storage perf logging, how to download and analyze the logs and also how to combine this anlysis with query engines like Spark and Hive. 


## Downloading and Analyzing WASB logs

Azure Storage provides [logs and metrics](https://docs.microsoft.com/en-us/azure/storage/common/storage-analytics) for all the requests. The logs are stored in the storage account in the following form ``https://<accountname>.blob.core.windows.net/$logs/<service-name>/YYYY/MM/DD/hhmm/<counter>.log``. Although, this format for logs is simple, it can be quite challenging to build tools and automatation around this format - especially if you want to be efficient. This was one of my motivation behind writing [azlogs](https://github.com/dharmeshkakadia/azlogs) - a tool for downloading logs for given timeperiod. I use it automatically [analyze latencies](https://github.com/hdinsight/HivePerformanceAutomation/blob/master/bin/perfdatascripts/getStoreLatency.sh) of WASB requests.

Lets see how you can use azlogs to download the logs and anlayze them.

1. Enable azure storage logging by following the [documentation](https://docs.microsoft.com/en-us/rest/api/storageservices/fileservices/enabling-storage-logging-and-accessing-log-data).

2. Download the azlogs tool.
    ```bash
    git clone https://github.com/dharmeshkakadia/azlogs && cd azlogs
    ```

3. Compile it using Maven.
    ```bash
    mvn package assembly:single 
    ```

4. Download the logs for a given time range. You need to provide the storage account name and access key along with start and end time for which you want to logs for.
    ```bash
    Usage: azlogs <AccountName> <AccountKey> <startDate(seconds since epoch)> <endDate(seconds since epoch)> [columns(sorted)]
    ```
    For example, to download the logs for storage account ``storage1`` from ``1476132794`` to ``1476132895``, you can use the following command.
    ```bash
    java -jar azlogs.jar storage1 67t2Mw== "1476132794" "1476132895" "request_start_time,operation_type,end_to_end_latency_in_ms" 2>debug_logs > output
    ```

5. The above command will produce an output CSV file(delimited by ;) that you can use to analyze with your favorite data analysis tool. I like to use [csvkit](https://csvkit.readthedocs.io/en/1.0.1/) for working with csv files on command line. It allows you to write a sql query against a csv file. For example, here is how to calculate ``avg``,``min`` and ``max`` latencies (from both client and service side) and the counts for various operations on WASB from above output logs using csvkit.
    ```bash
    csvsql -d ";" --query "select operation_type, count(*), avg(end_to_end_latency_in_ms), min(end_to_end_latency_in_ms), max(end_to_end_latency_in_ms), avg(server_latency_in_ms), min(server_latency_in_ms),max(server_latency_in_ms) from output group by operation_type"
    ```
    This would produce output similar to :

    {% gist a3080a2759a0ecefb7a0d99943239ec8 %}


## Analyzing storage performance of a Spark or hive query

We can use the above technique to get the storage logs for a given spark or hive query/job. This is assuming the storage account is only being used by the given query. This is easily achievable in the benchmark or performance debugging scenarios. 

At a high level, the steps for measureing the storage performance for a given spark/hive query:

1. Record the start time 
    ```bash 
    STARTTIME="`date +%s`"
    ```
2. Execute spark or hive job(s). 
    ```bash 
    spark-sql -e "select count(*) from hivesampletable"
    ```
    or if you are using hive 

    ```bash 
    hive -e "select count(*) from hivesampletable"
    ```
    Note that, you can run arbitrary commands here that interact with storage. 
    
3. Record the end time.
    ```bash 
    ENDTIME="`date +%s`"
    ```

4. Download the storage logs from start time to end time using the steps mentioned above. This logs will contain all the storage requests made during this time frame. 
    ```bash
    java -jar azlogs.jar storage1 67t2Mw== "$STARTTIME" "$ENDTIME" "request_start_time,operation_type,end_to_end_latency_in_ms" 2>debug_logs > output
    ```
5. Anlayze the storage logs stored in ``output`` file.


In the first section of this post, we saw how to calulate ``avg``, ``min`` and ``max`` of storage request latecy. While these are useful statistical summaries, [quartiles](https://en.wikipedia.org/wiki/Quartile) provide a much more useful descriptive statstics, especially in case of latency numbers. In performance analysis, we care about 99th, 99.9th, 99.99th percentile latencies very often.  

We will now see how to calculate 99th percentile of storage requests. You can run the following command to generate 99th percentile latency numbers for different types of operations :

```bash
csvsql -d ";" --query "select operation_type,E2E99thP from (select end_to_end_latency_in_ms,operation_type from output order by end_to_end_latency_in_ms asc limit cast(0.99*(select count(end_to_end_latency_in_ms) from output)as int)) group by operation_type" 
```

{% gist b6c1b29cd899f31020f6ddc8e130882c %}

By changing ``0.99`` to in above query to ``0.999`` or ``0.9999``, we can calcualte 99.9th or 99.99th percentile latency. We can combine the above queries to get a better picture of the requests success rates and latencies.

## Analyzing storage performance of your big data workload

While measuring storage latencies for individual queries are useful for debugging query performance, if we want to get a more complete picture of storage and query engine performance on cloud, we should run industry standard benchmarks like [tpch](https://github.com/dharmeshkakadia/tpch-hdinsight) and [tpcds](https://github.com/dharmeshkakadia/tpcds-hdinsight) and see the storage reuqests numbers. With little more [automation](https://github.com/hdinsight/HivePerformanceAutomation), we can generate the following summary of storage requests across different queries:

{% gist 7c2a3750298af7757ddde8714b84e3b5 %}

Remember, storage is just one part of the query engines performance, if we want to understand the query engine performance at a deeper level, we need to combine this with other resource performance data - namely network, CPU, memory. In the next post we will see how to achieve that. Till then go measure your storage performance!
