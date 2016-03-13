---
layout: post
title: How to write a Hive Hook
---

Hive Hooks are little known gems that can be used for many purposes - everything you always wanted to know about Hive hooks. In this post we will take a deeper look at what a Hive hook is and how to write and use a Hive hook.

##What is Hive?
For the readers unaware of [Hive](https://hive.apache.org), it provides an SQL interface to Hadoop. Hive is compiler that translates SQL (strictly speaking Hive Query Language - HQL, a variant of SQL) into a set of Mapreduce/Tez/Spark jobs. Thus, Hive is very instrumental in enabling non programmers to use Hadoop infrastructure. Traditionally, Hive had only one backend, namely MapReduce. But with recent versions, Hive supports [Spark](http://spark.apache.org) and [Tez](http://tez.apache.org) also as execution engines. This makes Hive a great tool for exploratory data analysis.

The following diagram and terms from the Hive documentation explains high level design of Hive with MapReduce backend.
![Hive design diagram](https://cwiki.apache.org/confluence/download/attachments/27362072/system_architecture.png?version=1&modificationDate=1414560669000&api=v2)

Driver – The component which receives the queries. This component implements the notion of session handles and provides execute and fetch APIs modeled on JDBC/ODBC interfaces.
Compiler – The component that parses the query, does semantic analysis on the different query blocks and query expressions and eventually generates an execution plan with the help of the table and partition metadata looked up from the metastore.
Metastore – The component that stores all the structure information of the various tables and partitions in the warehouse including column and column type information, the serializers and deserializers necessary to read and write data and the corresponding HDFS files where the data is stored.
Execution Engine – The component which executes the execution plan created by the compiler. The plan is a DAG of stages. The execution engine manages the dependencies between these different stages of the plan and executes these stages on the appropriate system components.
At a high level here are the steps that happen during the processing of a given query:

Driver.run() takes the command
HiveDriverRunHook.preDriverRun()
(HiveConf.ConfVars.HIVE_DRIVER_RUN_HOOKS)
Driver.compile() starts processing the command: creates the abstract syntax tree
AbstractSemanticAnalyzerHook.preAnalyze()
(HiveConf.ConfVars.SEMANTIC_ANALYZER_HOOK)
Semantic analysis
AbstractSemanticAnalyzerHook.postAnalyze()
(HiveConf.ConfVars.SEMANTIC_ANALYZER_HOOK)
Create and validate the query plan (physical plan)
Driver.execute() : ready to run the jobs
ExecuteWithHookContext.run()
(HiveConf.ConfVars.PREEXECHOOKS)
ExecDriver.execute() runs all the jobs
For each job at every HiveConf.ConfVars.HIVECOUNTERSPULLINTERVAL interval:
ClientStatsPublisher.run() is called to publish statistics
(HiveConf.ConfVars.CLIENTSTATSPUBLISHERS)
If a task fails: ExecuteWithHookContext.run()
(HiveConf.ConfVars.ONFAILUREHOOKS)
Finish all the tasks
ExecuteWithHookContext.run()
(HiveConf.ConfVars.POSTEXECHOOKS)
Before returning the result HiveDriverRunHook.postDriverRun()
( HiveConf.ConfVars.HIVE_DRIVER_RUN_HOOKS)
Return the result.

##What is a Hive Hook?
In general Hook is a mechanism for intercepting events, messages or function calls during processing. Hive hooks are mechanism to tie into the internal working of Hive without the need of recompiling Hive. Hooks in this sense provide ability to extend and integrate external functionality with Hive. In other words Hive hooks can be used to run/inject some code during various steps of query processing. Depending on the type of hook it can be invoked at different point during query processing.


Pre-execution hooks are invoked before the execution of the query by the execution engine begins. Note that at this point you have hive already has an optimized query plan for the execution ready.
Post-execution hooks are invoked after the execution of the query is finished and before the results are returned to the user.
Failure-execution hooks are invoked when the execution of the query fails.
Pre-driver-run and post-driver-run hooks are invoked before and after the driver is run on the query.
Pre-semantic-analyzer and Post-semantic-analyzer hooks are invoked before and after hive runs semantic analyzer on the query string.
Metastore initialization hooks are invoked when Hive metastore is initialized. If we want to log what new tables/databases are created in Hive to external services, then Metastore hooks are the place to do it. This can be used for example to keep HBase in sync with Hive metastore.
org.apache.hadoop.hive.metastore.HiveMetaHook interface defines the following methods that are invoked as part of metastore transections - create/drop a table. The Table object has all the necessary information about the table being processed like its name, database it is part of, Serializer, properties, columns etc.

public void preCreateTable(Table table) throws MetaException;

public void rollbackCreateTable(Table table) throws MetaException;

public void commitCreateTable(Table table) throws MetaException;

public void preDropTable(Table table) throws MetaException;

public void rollbackDropTable(Table table) throws MetaException;

public void commitDropTable(Table table, boolean deleteData) throws MetaException;

A hook can be used for any purpose you see appropriate.

Note, that Hooks are invoked in the normal processing path for Hive. So, avoid doing very costly operations in the Hive pre-hooks and metastore hooks.

Who are using them? In general not very well known. Partially because of the not so great documentation.

Hive is very much alive with Tez and Spark and it's quickly/has become/becoming de-facto standard for

There are many different kinds of Hook that Hive supports.

##Hive Hook API

We will now write an example Hive hook and setup it with hive. We will write a simple pre-execution hook that will write "Hello from the hook !!".

lets setup a project using maven.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>hive-hook-example</groupId>
    <artifactId>Hive-hook-example</artifactId>
    <version>1.0</version>

</project>
```

Now add the hive-exec package as a dependency to your project using,

```xml
    <dependencies>
        <dependency>
            <groupId>org.apache.hive</groupId>
            <artifactId>hive-exec</artifactId>
            <version>1.1.0</version>
        </dependency>
    </dependencies>
```

Now lets create a class that implements the hook interface. We will call our class HiveExampleHook which will implement the org.apache.hadoop.hive.ql.hooks.ExecuteWithHookContext. This interface has only one method with following signature,
     public void run(HookContext) throws Exception;
For now we will just put a single statement
     System.out.println("Hello from the hook !!");
If you want to see another simple Hive hook with a real use case you can check out YarnReservationHook. It uses Yarn's reservation API to reserve resources for given query just before the query starts the execution via a pre-execution- hook. We have another simple post-execution-hook that cleans up the reservation at the end of query.

###Resources:

1. http://stackoverflow.com/questions/17461932/hive-execution-hook
2. http://www.slideshare.net/julingks/apache-hive-hooksminwookim130813





