---
layout: post
published: false
title: RStudio on Kubernetes
---

R is very versatile language for data analysis and widely used for data science and exploration alongside python. [RStudio](https://www.rstudio.com/) is a great IDE for exploring data using R. RStudio has a lot of powerful [features](https://www.rstudio.com/products/rstudio/features/) for writing and debugging R code, but while using it on large data, it can be challanging due to:

* Scalability 
* Privacy and security of data
* Ability to connect R workflows with other worflows (Spark, Tensorflow etc.)

[Blobfuse]() allows data on Azure Blob Storage as as local files. 

We will see how we can deploy RStudio using [Kubernetes](https://kubernetes.io), Deploying RStudio on Kubernetes has many advantages :

* Allows exploration tools like RStudio also to be in controlled and secure environments.
* With combinations of blobfuse, makes sure the data never leaves the compliance boundary.
* Also makes RStudio available in web browser from anywhere. 
* RStudio, running on cluster can have a lot more resources that can be used by for exploration by R
* With cache interval, you can automatically cache the remote data for longer time as well, for better performance. 

Git link:

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

```
kubectl create -f git link TODO
```

Now, if you dont want to assign public end point to your RStudio deployment, you can access via local port-forwarding:
```
kubectl port-forward deploy/rstudio 8787:8787
```

Now you are ready to go : http://localhost:8787

and username/password pairs are X/X

Note that you can use similar deployment for deploying your Shiny (TODO link) apps on kubernetes.
