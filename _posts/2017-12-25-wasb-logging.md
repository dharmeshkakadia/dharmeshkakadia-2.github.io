---
layout: post
title: Analyzing Azure Storage Performance
published: false
---
I work on performance of Big data systems at [Azure HDInsight](https://azure.microsoft.com/en-us/services/hdinsight/) and as part of [benchmarking](https://azure.microsoft.com/en-us/blog/hdinsight-interactive-query-performance-benchmarks-and-integration-with-power-bi-direct-query/) many times I need to analyze the performance of the cloud storage. The performance is very important factor when deciding cloud solutions. In this post we will see how to analyze performance of [Azure Storage Blob (aka WASB)](https://azure.microsoft.com/en-us/services/storage/). We will see how to enable perf logging, how to download and analyze the logs. Even though there are public benchmarks available for theses systems, its important to measure performance for your workload. In that spirit, we will also see how to leverage storage logs for benchmarking big data workload. As an example, we will calculate 99th percentile latency of all the storage request made during execution of a hive query.


## Downloading and Analyzing WASB logs

Azure Storage provides [logs and metrics](https://docs.microsoft.com/en-us/azure/storage/common/storage-analytics) for all the requests. The logs are stored in the storage account in the following form ``https://<accountname>.blob.core.windows.net/$logs/<service-name>/YYYY/MM/DD/hhmm/<counter>.log``. Although, this format for logs is simple, it can be quite challenging to build tools and automatation. This was one of the motivation behind writing [azlogs](https://github.com/dharmeshkakadia/azlogs) - a tool for downloading logs for given timeperiod. I use it automatically [analyze latencies](https://github.com/hdinsight/HivePerformanceAutomation/blob/master/bin/perfdatascripts/getStoreLatency.sh) of WASB requests.

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

5. The above command will produce an output CSV file(delimited by ;) that you can use to analyze with your favorite data analysis tool. Mine happens to be [csvkit](https://csvkit.readthedocs.io/en/1.0.1/).

    For example, here is how to calculate ``avg``,``min`` and ``max`` latencies (from both client and service side) and the counts for various operations on WASB from above output logs.
    ```bash
    csvsql -d ";" --query "select operation_type, count(*), avg(end_to_end_latency_in_ms), min(end_to_end_latency_in_ms), max(end_to_end_latency_in_ms), avg(server_latency_in_ms), min(server_latency_in_ms),max(server_latency_in_ms) from output group by operation_type"
    ```
    This would produce output similar to :

    **operation\_type**|**count(*)**|**avg(end\_to\_end\_latency\_in\_ms)**|**min(end\_to\_end\_latency\_in\_ms)**|**max(end\_to\_end\_latency\_in\_ms)**|**avg(server\_latency\_in\_ms)**|**min(server\_latency\_in\_ms)**|**max(server\_latency\_in\_ms)**| 
    :-----|-----:|-----:|-----:|-----:|-----:|-----:|-----:|
    CopyBlob|60|44.18333333|6|296|44.18333333|6|296
    CopyBlobDestination|60|44.18333333|6|296|44.18333333|6|296
    CopyBlobSource|60|44.18333333|6|296|44.18333333|6|296
    DeleteBlob|62|5.290322581|2|58|5.290322581|2|58
    GetBlob|48491|100.4425564|2|5754|73.59421336|1|722
    GetBlobProperties|68634|2.367631203|1|206|2.367631203|1|206
    GetContainerProperties|2605|2.731669866|1|138|2.731669866|1|138
    GetPageRegions|78|2.064102564|1|3|1.987179487|1|3
    ListBlobs|2485|3.388732394|1|175|2.707847082|1|175
    PutBlob|6|5.333333333|5|7|5.333333333|5|7
    PutBlock|54|1435.333333|76|2803|1421.148148|63|2716
    PutBlockList|56|507.6785714|4|1895|507.6785714|4|1895
    PutPage|38|29.81578947|4|103|22.57894737|4|77
    SetBlobMetadata|7|4.142857143|3|5|4.142857143|3|5
    SetBlobProperties|86|34.97674419|3|93|34.97674419|3|93


## How to analyze storage performance for Spark or hive queries

We can use the above technique to get the storage logs for a given spark or hive query/job. This is assuming the storage account is only being used by the given query. This is easily achievable in the benchmark or performance debugging scenarios. 

So, the steps for measureing the storage performance for a given spark/hive query:

1. Note the start time.
2. Execute spark or hive job. 
3. Note the end time.
4. Download the storage logs from start time to end time using the steps mentioned above. This logs will contain all the storage requests made during this time frame. 
5. Anlayze the storage logs.

In the above output we saw how to calulate avg, min and max of storage request latecy. While this are useful summaries, [quartiles](https://en.wikipedia.org/wiki/Quartile) provide a much more useful descriptive statstics, especially in case of latency numbers. In performance analysis, we care about 99th, 99.9th, 99.99th percentile latencies very often.  

We will now see how to calculate 99th percentile of storage requests. You can run the following command to generate 99th percentile latency numbers for different types of operations :

```bash
csvsql -d ";" --query "select operation_type,E2E99thP from (select end_to_end_latency_in_ms,operation_type from output order by end_to_end_latency_in_ms asc limit cast(0.99*(select count(end_to_end_latency_in_ms) from output)as int)) group by operation_type" 
```

**operation\_type**|**E2E99thP**|
:-----|-----:|
CopyBlob|95
CopyBlobDestination|95
CopyBlobSource|95
DeleteBlob|38
GetBlob|1251
GetBlobProperties|147
GetContainerProperties|127
GetPageRegions|4
ListBlobs|158
PutBlob|5
PutBlock|158
PutBlockList|63
PutPage|207
SetBlobMetadata|4
SetBlobProperties|39

By changing ``0.99`` to in above query to ``0.999`` or ``0.9999``, we can calcualte 99.9th or 99.99th percentile latency. We can combine the above queries to get a better picture of the requests success rates and latencies.

While measuring storage latencies for individual queries are useful for debugging query performance, but if we want to get a more complete picture of storage and query engine performance on cloud, we should run industry standard benchmarks like [tpch](https://github.com/dharmeshkakadia/tpch-hdinsight) and [tpcds](https://github.com/dharmeshkakadia/tpcds-hdinsight) and see the storage reuqests numbers. With little more [automation](https://github.com/hdinsight/HivePerformanceAutomation), we can generate the following summary of storage requests across different queries:

**Query**|**operation\_type**|**count(*)**|**avg(end\_to\_end\_latency\_in\_ms)**|**min(end\_to\_end\_latency\_in\_ms)**|**max(end\_to\_end\_latency\_in\_ms)**|**avg(server\_latency\_in\_ms)**|**min(server\_latency\_in\_ms)**|**max(server\_latency\_in\_ms)**|**E2E99thP**|**E2E999thP**|**E2E9999thP**
:-----:|:-----|-----:|-----:|-----:|-----:|-----:|-----:|-----:|-----:|-----:|-----:
q10|CopyBlob|50|17.76|7|95|17.76|7|95|95|95|95
q10|CopyBlobDestination|50|17.76|7|95|17.76|7|95|95|95|95
q10|CopyBlobSource|50|17.76|7|95|17.76|7|95|95|95|95
q10|DeleteBlob|52|4.980769231|3|38|4.980769231|3|38|38|38|38
q10|GetBlob|31242|199.13293|1|13570|76.33883874|1|667|1251|4287|9187
q10|GetBlobProperties|56321|2.278102306|0|147|2.278102306|0|147|147|147|147
q10|GetContainerProperties|2549|2.770498235|1|127|2.770498235|1|127|127|127|127
q10|GetPageRegions|123|2.06504065|1|4|1.975609756|1|4|4|4|4
q10|ListBlobs|2269|3.374614368|1|158|2.927721463|1|158|158|158|158
q10|PutBlob|2|5|5|5|5|5|5|5|5|5
q10|PutBlock|39|72.15384615|5|158|58.61538462|5|148|158|158|158
q10|PutBlockList|51|12.11764706|4|63|12.09803922|4|63|63|63|63
q10|PutPage|43|33.3255814|2|207|22|2|107|207|207|207
q10|SetBlobMetadata|2|3.5|3|4|3.5|3|4|4|4|4
q10|SetBlobProperties|77|4.597402597|2|39|4.597402597|2|39|39|39|39
q11|CopyBlob|38|11.89473684|7|28|11.89473684|7|28|28|28|28
q11|CopyBlobDestination|38|11.89473684|7|28|11.89473684|7|28|28|28|28
q11|CopyBlobSource|38|11.89473684|7|28|11.89473684|7|28|28|28|28
q11|DeleteBlob|39|3.923076923|3|15|3.923076923|3|15|15|15|15
q11|GetBlob|11524|89.72544255|1|1312|62.7711732|1|1298|357|687|1208
q11|GetBlobProperties|28001|2.249348238|1|147|2.249348238|1|147|147|147|147
q11|GetContainerProperties|1693|3.069108092|1|99|3.069108092|1|99|99|99|99
q11|GetPageRegions|20|2.1|2|3|2.05|2|3|3|3|3
q11|ListBlobs|174|11.31034483|1|338|5.701149425|1|232|338|338|338
q11|PutBlob|6|5|4|6|5|4|6|6|6|6
q11|PutBlock|19|22.26315789|14|38|19.57894737|12|35|38|38|38
q11|PutBlockList|40|7|4|21|7|4|21|21|21|21
q11|PutPage|19|31.78947368|3|174|23.21052632|3|79|174|174|174
q11|SetBlobMetadata|7|3.428571429|3|4|3.428571429|3|4|4|4|4
q11|SetBlobProperties|61|5.524590164|3|26|5.524590164|3|26|26|26|26
q13|CopyBlob|40|31.075|7|113|31.075|7|113|113|113|113
q13|CopyBlobDestination|40|31.075|7|113|31.075|7|113|113|113|113
q13|CopyBlobSource|40|31.075|7|113|31.075|7|113|113|113|113
q13|DeleteBlob|40|4.775|3|8|4.775|3|8|8|8|8
q13|GetBlob|18331|87.09426654|2|1410|58.83159675|1|1380|350|704|1189
q13|GetBlobProperties|41538|2.208363426|1|138|2.208363426|1|138|138|138|138
q13|GetContainerProperties|2347|2.756284619|1|120|2.756284619|1|120|120|120|120
q13|GetPageRegions|47|2.276595745|1|12|2.14893617|1|11|12|12|12
q13|ListBlobs|2044|3.11741683|1|116|2.6037182|1|116|116|116|116
q13|PutBlob|3|6|4|9|6|4|9|9|9|9
q13|PutBlock|43|719.372093|96|1189|707.0930233|83|1176|251|709|1189
q13|PutBlockList|43|195.2093023|4|1014|195.1860465|4|1014|240|702|1014
q13|PutPage|28|43.10714286|3|151|29.57142857|3|126|151|151|151
q13|SetBlobMetadata|4|3.25|3|4|3.25|3|4|4|4|4
q13|SetBlobProperties|65|14.83076923|3|45|14.83076923|3|45|45|45|45

That's it for now! Go measure your storage performance!
