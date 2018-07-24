---
layout: post
published: true
title: Compiling hive for a non-release hadoop version
---


We have been working on many interesting things around [Perforator](https://www.microsoft.com/en-us/research/project/perforator-2/) like extending the core model to other systems like hive, tez etc. At MSR, we developed on hadoop-yarn trunk and have deployed that with a version name `3.0.0-SNAPSHOT`. and for a lot of other reasons, we can't just rename the version. I have struggled a bit in last few days to run hive on top of the non-release version like ours and this blog highlights my solution.

While hive documentation have step to [compile from source](https://cwiki.apache.org/confluence/display/Hive/GettingStarted) I could not find any documentation on how to compile for a version not yet "integrated" with hive. I was hoping to find at least some information on this from [developer page](https://cwiki.apache.org/confluence/display/Hive/HiveDeveloperFAQ) of hive. Surprisingly enough, I didn't get anything there. Looking at the pom.xml, I had an early impression that, just changing the `0.23-hadoop-version` in the `pom.xml` would do the trick. But it turns out that hive on starting, calls the hadoop version command to decide what shims to load. and thus will fail with unrecognized hadoop version error, like following.

{% gist 009b4a268e2a34162742 %}

There is an important piece of information as highlighted above, `ShimLoads.java` is the culprit, as before loading the Shims for a given hadoop version it does a sanity check that the hadoop version number is valid. so just go ahead an make sure that this tests passes. I know this test is important, but if you are in situation like me,  just go ahead and add the following lines in the file.

```
$ vim shims/common/src/main/java/org/apache/hadoop/hive/shims/ShimLoader.java
```

and add the case statement for your version number. I will add "case 3:" as shown below.

{% gist 7a3821c07240826920b3 %}

Now you can build hive with following command.

```
$ mvn clean install -Phadoop-2,dist
```

After successful completion of the above command, you would find the packages hive distribution in the `packaging/target/` folder.

### Gotchas

1. Don't use JDK 7 otherwise you might hive will fail to compile.
[https://issues.apache.org/jira/browse/HIVE-3197](https://issues.apache.org/jira/browse/HIVE-3197)
[https://issues.apache.org/jira/browse/HIVE-3384](https://issues.apache.org/jira/browse/HIVE-3384)

2. Contrib module in current hive trunk is broken by the dependencies on the package org.apache.hadoop.record, which is moved to hadoop-streaming project and then reverted.
[https://issues.apache.org/jira/browse/HIVE-7077](https://issues.apache.org/jira/browse/HIVE-7077)
[https://issues.apache.org/jira/browse/HADOOP-10474](https://issues.apache.org/jira/browse/HADOOP-10474)
  If you encounter this, there is a simple workaround for that. You can just build the `contrib` module with version of hadoop that is not effected by above change. Instead of doing any changes to the pom file etc, I simply built it with the `hadoop-1`. While this is likely to be fixed in the future version,here are the commands to workaround,

    ```
     $ cd contrib
     $ mvn clean install -Phadoop-1,dist
     $ cd ..
     $ mvn install -Phadoop-2,dist
    ```

    Note that we have removed clean from the goals, so as to avoid compiling the contrib module with the `hadoop-2`. Since `mvn` sees that the module is already compiled, it just goes ahead with the rest of hive.
