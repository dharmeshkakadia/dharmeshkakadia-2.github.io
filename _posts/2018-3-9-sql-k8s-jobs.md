---
published: false
title: Automate SQL server data pipelines with Kubernetes
---
Kubernetes provides a great way to run modern infrastructure. SQL server is a widely deployed database. When you combine these two, you get a robust way of running a data pipeline using a modern platform.

Data pipelines are large part of all data infrastructure. The need to move data between different systems, is almost universal and tools/process to achieve this is generally referred to as a data pipeline. In this post we will see how we can leverage [Kubernetes jobs API](https://kubernetes.io/docs/concepts/workloads/controllers/jobs-run-to-completion/) to build and run data pipelines. This is a great way to integrate data pipelines into CI/CD practices too.

Following steps will create an example SQL pipeline and run it against SQL server using Kubernetes. We will be running a very simple query to list all the tables. 

1. Lets define our job in the file ``sql-k8s-job.yaml``.

    ```yml
    apiVersion: batch/v1
    kind: Job
    metadata:
    name: sqljob
    spec:
    template:
        spec:
        containers:
        - name: sqljobcontainer
            image: microsoft/mssql-tools
            command: ["/opt/mssql-tools/bin/sqlcmd"]
            args: [ "-S", "mysqlserver.database.windows.net", "-d", "mydatabase", "-U", "User", "-P", "PassWord", "-I", "-Q", "SELECT name FROM sys.tables" ]
        restartPolicy: Never
    ```

    Here, we are specifying that this is a job definition(``kind: Job``) with the name ``sqljob``. The spec part is similar to other container specifications. We are specifying it to create a container with a name ``sqljobcontainer`` with the image ``microsoft/mssql-tools``. This image has all MSSQL tools installed to connect to a remote MSSQL instance. We are also specifying that it should run ``sqlcmd`` command with the specified arguments, including server, database, password and query when it starts the container. Note that, I am specifying password in the job definition file here just for simplicity, you should use [kubernetes secrets](https://kubernetes.io/docs/concepts/configuration/secret/) when doing anything serious. 

2. Lets run it. You can run it locally using [minikube](https://kubernetes.io/docs/getting-started-guides/minikube/) or on cloud.

    ```
    kubectl create -f sql-k8s-job.yaml
    
    job "sqljob" created
    ```

3. You can see the details on the job.
    ```
    kubectl describe jobs/sqljob

    Name:           sqljob
    Namespace:      default
    Selector:       controller-uid=85530e4e-2eef-11e8-9e3f-92f68014defe
    Labels:         controller-uid=85530e4e-2eef-11e8-9e3f-92f68014defe
                    job-name=sqljob
    Annotations:    <none>
    Parallelism:    1
    Completions:    1
    Start Time:     Fri, 23 Mar 2018 16:11:30 -0700
    Pods Statuses:  1 Running / 0 Succeeded / 2 Failed
    Pod Template:
    Labels:  controller-uid=85530e4e-2eef-11e8-9e3f-92f68014defe
            job-name=sqljob
    Containers:
    sqljobcontainer:
        Image:  microsoft/mssql-tools
        Port:   <none>
        Command:
        /opt/mssql-tools/bin/sqlcmd
        Args:
        -S
        mysqlserver.database.windows.net
        -d
        mydatabase
        -U
        User
        -P
        PassWord
        -I
        -Q
        SELECT name FROM sys.tables
        Environment:  <none>
        Mounts:       <none>
    Volumes:        <none>
    Events:
    Type    Reason            Age   From            Message
    ----    ------            ----  ----            -------
    Normal  SuccessfulCreate  30s   job-controller  Created pod: sqljob-qsdtg
    Normal  SuccessfulCreate  20s   job-controller  Created pod: sqljob-pws2m
    Normal  SuccessfulCreate  10s   job-controller  Created pod: sqljob-lb2dz
    ```
    You can also see the job on the kubernetes dashboard. You can open the kubernetes dashboard using 

    ```
    minikube dashboard
    ```
    You can see the job under jobs section in the dashboard.

    ![sqljib-k8s-dashboard]({{site.baseurl}}/images/sql-k8s-job.png)

3. Lets see the output from the job.

    ```
    kubectl logs jobs/sqljob
    ```
    You should see the list of all the tables in your database.

4. Finally you can delete the job using

    ```
    kubectl delete jobs/sqljob

    job "sqljob" deleted
    ```

    Now that you have are comfortable with this job, you can easily convert this into a recurring job. Kubernetes jobs support for [cron jobs](https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/). You can include the cron syntax schedule in the container spec to convert a job into a cron job. For example, by including ``schedule: "0 * * * *"`` in the ``spec`` section of the job, your job will run every 1-hour. Crontab syntax is hard to remember and undertstand, but luckily you can just use [crontab.guru](https://crontab.guru/).

Thats it. Go build your pipeline !
