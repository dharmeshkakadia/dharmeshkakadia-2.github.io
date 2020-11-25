---
published: false
layout: post
title: Machine Learning in Systems
---

So many possibilities.

Starting to happen.

The compilation/metadata service. Captures lineage. Knows data access pattern. Knows the execution pattern across queries. Is leveraged by scheduler.

Learning to Optimize/Schedule. In line with joint/co-optimization of logical and physical plan in the big data world.

CMU Self-driving databases.
Some of the berkeley work.
MSR paper.
Tuning config in Big data on cloud for arbtrary query is already beyond humans. Example configs of choosing cluster size for the given workload. Perforator. 

There is tradeoff both ways. 
Traditional databases could only spend limited resources on optimization, but a optimization service with 50k nodes can spend huge amount of resoruces to decide better plans, if it can result into sizable savings in cluster resources.
Also, latency in making decision can be tolerated.

But on the other hand, the optimization problem becomes extremely hard once you compine all things - cloud, engines, and so on.

Automatically selecting the best engine for the query.
Things like lambda present other set of challenges - latency is cruicial. But relatively easy to "test out" different decisions - say which node to run the function on - since its highly likly that you will have future invocations.
But not easy to isolate the results due to lots of factors - especially other workload/functions running on the shared cluster. 

Data <--> System loop. Goes both way. The ML security work in other way loop.

Cost optimizating in cloud.

Many many monitoring systems in large scale infrastructure.

Scheduling. Can it learn all the policies that is being followed? How much data we need? 

Advantage compared to tradditioanl ml problems
We can get data easily. Not sure we can get labelled data easily.

When can we trust the ML ?

Philosophy

Would we ever trust ML enough to put it in compiler optimizations? That to me sounds like the last step. :)

