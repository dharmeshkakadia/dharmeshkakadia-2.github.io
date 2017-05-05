---
layout: post
title: Presto on HDInsight
---

How to run Presto on HDInsight
If you are faimilier with presto and want to 

# What is Presto?
Presto is a distributed SQL query engine for big data.
Its known for being fast

It supports querying data in wide range of format including Parquet, ORC, Text, RCFile and so on.
The presto 

# Presto Architecture
To understand how does presto works, lets looks at the presto architecture. The below figure is taken from 

# Use cases
While presto is very successfully used by nuber of orgnizations for their fast data anlysis needs,
One of the prime aspect that caught my attention was the ability to query various data sources in a single query. This is so magical ✨, let me give you an example,


This obviates the need to bring the all the data manged under the same system. This in my opinion is so important since, the world where each system wants to be the _only_ system to store and process data.
The reality however is that each system makes different tradeoffs and are fit and serve only part of the larger picture.

# Airpal
Airpal is the web query interface for presto

# Who is using Presto?
Everyone

# Step by Step instructions

# Customizing installation

# Inner details
If you are interestred in the details of what is the above script doing, let me break it down.

How to run presto TPCDS article link

https://github.com/dharmeshkakadia/presto-hdinsight

https://prestodb.io/
