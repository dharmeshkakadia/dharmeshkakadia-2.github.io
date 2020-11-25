---
layout: post
published: true
title: Versatile RStudio development environment on Kubernetes
---

R is very versatile language for data analysis and widely used for data science and exploration alongside python. [RStudio](https://www.rstudio.com/) is a great IDE for exploring data using R. RStudio has a lot of powerful [features](https://www.rstudio.com/products/rstudio/features/) for writing and debugging R code, but while using it on large data, it can be challenging due to:

* Scalability
* Privacy and security of data
* Ability to connect R workflows with other tools (Spark, Tensorflow etc.)
* Backing up the R code automatically

We solve these challenges by running [RStudio on Kubernetes](#deploying-rstudio-on-k8s) and using [Blobfuse](#blobfuse-for-remote-data-access) for remote data access. 

## Deploying RStudio on k8s

First, we will see how we can deploy RStudio using [Kubernetes](https://kubernetes.io), Deploying RStudio on Kubernetes has many advantages :

* Allows exploration tools like RStudio also to be in controlled and secure environments.
* With combinations of blobfuse, makes sure the data never leaves the compliance boundary.
* Also makes RStudio available in web browser from anywhere. 
* RStudio, running on cluster can have a lot more resources that can be used by for exploration by R.
* With cache interval, you can automatically cache the remote data for longer time as well, for better performance. 

We will create a Kubernetes [deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/) for RStudio. The following YAML describes our RStudio deployment. Dont worry if you don't all the fields in the YAML, you don't need to understand all the kubernetes concepts for now.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: rstudio
  labels:
    name: rstudio
spec:
  replicas: 1
  selector:
    matchLabels:
      name: rstudio
  template:
    metadata:
      labels:
        name: rstudio
    spec:
      containers:
      - name : rstudio
        image: rocker/rstudio 
        imagePullPolicy: "Always"
        ports:
        - containerPort: 8787
          protocol: TCP
        command:
         - "/bin/bash"
         - "-c"
         - "--"
        args :
         - 'rstudio-server start ; sleep infinity'
```

I have put these configuration files on github here [dharmeshkakadia/rstudio-k8s](https://github.com/dharmeshkakadia/rstudio-k8s). You can deploy the above YAML directly from github link with:
```
kubectl create -f https://raw.githubusercontent.com/dharmeshkakadia/rstudio-k8s/master/rstudio.yaml
```

The above deployment doesn't assign public end point to your RStudio deployment and you can access via local port-forwarding:
```
kubectl port-forward deploy/rstudio 8787:8787
```

That's it! Now you are ready to use RStudio. Go to [http://localhost:8787](http://localhost:8787) and use username and password as `rstudio`.

![Rstudio]({{site.baseurl}}/images/rstudio-k8s.png)


## Blobfuse for remote data access

[Blobfuse](https://github.com/Azure/azure-storage-fuse) allows access to remote blob storage data as if it was part of local file system. This makes it possible to work with many packages that doesn't yet work with remote storage natively. This also makes it simple for developers to be hidden from operational aspect of how the data is managed. We use [blobfuse kubernetes volume drivers](https://github.com/Azure/kubernetes-volume-drivers/tree/master/flexvolume/blobfuse) to integrate blobfuse with Kubernetes. With this setup, we can allows access to data on Azure Blob Storage as as local files from with Kubernetes constructs like pods. You need to install blobfuse on the cluster, by following [instructions](https://github.com/Azure/kubernetes-volume-drivers/tree/master/flexvolume/blobfuse). Note that using blobfuse is not required to use RStudio Kubernetes, but only required for integration with Azure Storage.

You will need to create a [Kubernetes Secret](https://kubernetes.io/docs/concepts/configuration/secret/) that allows access to the given storage account. You can use the command similar to the below, replacing your account name and storage key. Note that in production environment, this should not be done manually, but secret management solutions like [Azure Key Vault](https://docs.microsoft.com/en-us/azure/key-vault/) with your CI/CD pipelines.

```
kubectl create secret generic blofuse-datasecret --from-literal accountname=storage-account-name --from-literal accountkey="fJg4..0A==" --type="azure/blobfuse"
```

Here is the full YAML with volume mounts sections addded. We are instructing Kubernetes to use the secret we just created (`blobfuse-datasecret`) and mount `datacontainer-name` from the storage account at location `/data/` in the container. Of course you should change the value of `datacontainer-name` with the name of the storage container you want to access. 

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: rstudio
  labels:
    name: rstudio
spec:
  replicas: 1
  selector:
    matchLabels:
      name: rstudio
  template:
    metadata:
      labels:
        name: rstudio
    spec:
      containers:
      - name : rstudio
        image: rocker/rstudio 
        imagePullPolicy: "Always"
        ports:
        - containerPort: 8787
          protocol: TCP
        command:
         - "/bin/bash"
         - "-c"
         - "--"
        args :
         - 'rstudio-server start ; sleep infinity'
        volumeMounts:
        - name: data
          mountPath: /data
      volumes:
      - name: data
        flexVolume:
          driver: "azure/blobfuse"
          secretRef:
            name: blofuse-datasecret
          options:
            container: datacontainer-name
```

You can deploy the above YAML with:
```
kubectl create -f rstudio-blobfuse.yaml
```

That's it ! Now when using RStudio, you can read files under `/data` as with normal file APIs and use the remote data as if they were local files. We can use the same mechanism to backup R code from a `local` folder to Azure Blob. Also, you since you can have multiple volumes mounted, you can easily use conventions like `/userdata`, `/researchdata` and so on to have _all_ of various datasets available to you during exploration.

There are many more possibilities, by integrating data frameworks and Kubernetes. For example, you can use similar deployment for deploying your [Shiny](https://shiny.rstudio.com/) apps on kubernetes, which will auto scale based on your traffic or load. You can use also deploy R ETL scripts as Kubernetes [Jobs](https://kubernetes.io/docs/concepts/workloads/controllers/jobs-run-to-completion/) or [CronJobs](https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/) and get fault tolerance alerts etc for free. We use such Kubernetes constructs across our entire data/AI stack with Spark, Tensorflow, Jupyter etc. and had a lot of success with it. 

Have fun data hacking !
