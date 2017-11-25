---
published: false
---
## Cloud Native Data Systems

 Cloud Native vs On-Prim design decisions
 
Some of the decisions made differently if you are designing data system for cloud vs on-prim.
 
Installation/upgrade is once in a year thing. So ok to take 60 mins to do it.
 
Ambari installation
 
People provisioning cluster and using are very different and thus have those profile.
Ambari used by operators.
JDBC/ODBC used by data scientists.
 
Resources are fixed
High reliance on sharing resources and isolation
 
Since the choice of platform is a long term (and often top-down) any focus on productivity and UI is secondary.
Cloud you need a better experience, otherwise people are going to leave early.
 
Reliability
People are going to isolate new testing/ dev on separate
 
Recovery can be slow on prim since you are already paying for it, on cloud it needs to be fast to discard/recover.
 
Network is bottleneck on prim, no design for network latency or unavailability.
 
 