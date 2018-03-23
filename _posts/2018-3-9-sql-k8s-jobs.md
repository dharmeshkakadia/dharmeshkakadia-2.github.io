---
published: false
title: Automate SQL server data pipelines with Kubernetes
---
Kubernetes provides a great way to run modern infrastructure. SQL server is a widely deployed database.
We can leverage [Kubernetes jobs API](https://kubernetes.io/docs/concepts/workloads/controllers/jobs-run-to-completion/) to build and run data pipelines.

Why you might want to do this?



Below are the steps to create an example SQL pipeline and run it against SQL server using Kubernetes. We will be running a very simple query using 

1. Lets define our job in the file ``sqljob.yaml``.


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

    Here, We are specifying that this is a job definition(``kind: Job``) with the name ``sqljob``. The spec part is similar to other container specification. We are specifying it to create a container with a name ``sqljobcontainer`` with the image ``microsoft/mssql-tools``. This image has all MSSQL tools installed. We are also specifying that it should run ``sqlcmd`` command with the specified arguments, including server, database, password and query when it starts the container. Note that, I am specifying password in the job definition file here just for simplicity, you should use [kubernetes secrets](https://kubernetes.io/docs/concepts/configuration/secret/) when doing anything serious. 


2. Lets run it. You can run it locally using [minikube](https://kubernetes.io/docs/getting-started-guides/minikube/) or on cloud.

    ```
    kubectl create -f sqljob.yaml
    ```

3. You can see the details on the job.
    ```
    describe

    ```
    You can also see the job on the kubernetes dashboard. You can open the kubernetes dashboard using 

    ```
    minikube dashboard
    ```
    [screenshot]

3. Lets see the output from the job.
    ```
    kubectl logs jobs/sqljob
    ```
    

4. Finally you can delete the job using
    ```
    kubectl delete jobs/sqljob
    ```

 and its logs in the kubernetes dashboard.

Thats it !
