---
published: false
---
## Analyzing WASB server logs

Why?
WASB is critical.
We need to know how is it doing.

One of the motivation behind writing this tool was to be able to automate latency analysis of WASB.
https://github.com/dharmeshkakadia/azlogs

step by step
1. Enable azure storage logging by following the [documentation](https://docs.microsoft.com/en-us/rest/api/storageservices/fileservices/enabling-storage-logging-and-accessing-log-data).

2. Download the azlogs
```
git clone https://github.com/dharmeshkakadia/azlogs && cd azlogs
```

3. Compile it using Maven.
```
mvn package assembly:single 
```

4. Download the logs for a given timerange.
```
Usage: azlogs <AccountName> <AccountKey>startDate(seconds since epoch) endDate(seconds since epoch) [columns(sorted)]

For example
```
java -jar azlogs.jar storage1 67t2Mw== "1476132794" "1476132895" "request_start_time,operation_type,end_to_end_latency_in_ms" 2>debug_logs > output
```

5. The above command will produce an output CSV file that you can use to analyze with yout favourite analysis tool. Mine happens to be [csvkit](https://csvkit.readthedocs.io/en/1.0.1/).

For example, below example avg,min,max latency for various operations on WASB.
```
csvsql -d ";" --query "select operation_type, count(*), avg(end_to_end_latency_in_ms), min(end_to_end_latency_in_ms), max(end_to_end_latency_in_ms), avg(server_latency_in_ms), min(server_latency_in_ms),max(server_latency_in_ms) from output group by operation_type"
```

sample output

analyze 99th percentile latency

sample output


