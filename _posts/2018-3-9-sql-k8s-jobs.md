---
published: false
title: Automate SQL server data pipelines with Kubernetes
---
Kubernetes provides a great way to do bunch of things.'
We can leverage Kubernetes jobs API to build and run data pipelines.

Why you might want to do this?

Below are the steps to 

1. Lets define out job.


    ```yml
    apiVersion: batch/v1
    kind: Job
    metadata:
    name: gdpr
    spec:
    template:
        spec:
        containers:
        - name: gdpr
            image: microsoft/mssql-tools
            command: ["/opt/mssql-tools/bin/sqlcmd"]
            args: [ "-S", "mysqlserver.database.windows.net", "-d", "mydatabase", "-U", "User", "-P", "PassWord", "-I", "-Q", "SELECT name FROM sys.tables" ]
        restartPolicy: Never
    ```


2. Lets run it. You can run it locally using minikube[link] or on cloud.

3. Lets see the output from the job.
  
    
Thats it !
