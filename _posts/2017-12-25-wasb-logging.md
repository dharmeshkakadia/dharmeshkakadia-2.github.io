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


## How to analyze storage performance for hive queries

This 

```	csvsql -d ";" --query "select operation_type,E2E99thP from (select end_to_end_latency_in_ms,operation_type from output order by end_to_end_latency_in_ms asc limit cast(0.99*(select count(end_to_end_latency_in_ms) from output)as int)) group by operation_type" 
```
Here is the sample output

**Query**|**operation\_type**|**E2E99thP**|
:-----|:-----|-----:|
q10|CopyBlob|95
q10|CopyBlobDestination|95
q10|CopyBlobSource|95
q10|DeleteBlob|38
q10|GetBlob|1251
q10|GetBlobProperties|147
q10|GetContainerProperties|127
q10|GetPageRegions|4
q10|ListBlobs|158
q10|PutBlob|5
q10|PutBlock|158
q10|PutBlockList|63
q10|PutPage|207
q10|SetBlobMetadata|4
q10|SetBlobProperties|39

By changing the ``0.99`` to ``0.999`` we can calcualte 99.9th percentile latency. 

We can combine the above queries to produce the following summary:

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
