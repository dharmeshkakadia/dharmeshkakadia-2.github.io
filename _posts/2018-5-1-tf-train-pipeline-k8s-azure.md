---
published: false
title: Create Tensorflow training pipeline with Azure storage and Kubernetes
---
Kubernetes 

steps and screenshots

This will be long

Full API access 

Fault tolerance

Operational visibility 

Data lives on blob.
Use Blobfuse.
Use CI/CD post as a reference.
How to mount NVidia drivers.
How to mount blob.

Install blobfuse flexdriver on the cluster
This is needed once per cluster.
```bash
kubectl create -f https://raw.githubusercontent.com/andyzhangx/kubernetes-drivers/master/flexvolume/blobfuse/deployment/blobfuse-flexvol-installer-1.9.yaml
```
Create secret using blob keys
This is needed to be done once per storage account/container. Follow Naming conventions for secrets for data for adding secrets. Here is an example of adding it manually for testing. In production, it should be deployed using Naming conventions for secrets for data
```bash
kubectl create secret generic blobfusecreds --from-literal accountname=sparkdkakadia --from-literal accountkey="4gIguFMiymTI4BojDYUZfcgjYqAP6T+/eUXWH9RzJPQAlQpUsT1+ctZV+I55A==" --type="azure/blobfuse"
```
Create pod with volume spec 
You need to specify volume spec and volumemount in the container spec. Example:


```yaml
apiVersion: v1
kind: Pod
metadata:
  name: spark-flex-blobfuse
spec:
  containers:
  - name: spark-flex-blobfuse
    image: nginx
    volumeMounts:
    - name: test
      mountPath: /data
  volumes:
  - name: test
    flexVolume:
      driver: "azure/blobfuse"
      secretRef:
        name: blobfusecreds
      options:
        container: sparkdkakadia
```        
Best practices:
While mounting the containers, the mountPath should be same as container name. This would help in debugging and code reading.
Volume name should be descriptive. We recommend it to be same as container name. 

This guide describes how to write a TensorFlow training pipeline. This uses Azure GPUs via Kubernetes with data on Blob. This is the our strongly recommended way of building TensorFlow enabled training pipelines. See the Preprocess → Train → Serving portion of the Smart Classifier diagram for a detailed diagram of how this is expected to work.

Get a GPU kubernetes cluster
If you need GPU for your pipelines, make sure your Kubernetes cluster has GPU nodes in it. The GPU cluster can be created by following Setup Microservices Infrastructure and CI/CD#CreateaKubernetesCluster: guide. The node type we recommend for TensorFlow is Standard_ND24s.

Writing the TF training pipeline
Most of the steps are similar to How to write data pipelines and you should read it.

We recommend every new code reside in the shared data-analytics repo: https://ghe-us.microsoft.com/team-mdl/data-analytics. If you are building a newer code/service, you should create a new folder under it. See other folders in the repo for examples.
Write your TensorFlow code. Its best practice to read config - including data paths - as environment variables.

Write a dockerfile specifies how to build the image. If you are not using additonal libraries, it should be pretty much just adding your code on top of ``tensorflow:latest-gpu`` image. Here is one example.
```dockerfile
FROM tensorflow/tensorflow:latest-gpu
 
COPY . /code
 
WORKDIR /code
```
Please follow Naming conventions for secrets for data and Secrets deployment via KeyVault-VSTS-Kubernetes to inject Azure Blob key as secrets. This will be how you access data on Blob for training.

Write a Kubernetes cron job YAML to run your training code regularly. Like a normal pipeline, you want your deployment files under ops/k8s folder. There are couple of things you might have to add compared to normal cron jobs. 

Specify how many GPUs the job would be using. You will specify this as a value of ``alpha.kubernetes.io/nvidia-gpu`` under ``container`` spec. 
```yaml
resources:
    limits:
        alpha.kubernetes.io/nvidia-gpu: 1

Mount the Nvidia driver (you can pretty much copy paste this). This is specified in two parts: (1) where the drivers are on the host, and (2) where to mount them in the container. 

volumes: # Where the drivers are located on the node
    - name: lib
        hostPath:
            path: /usr/local/nvidia
volumeMounts: # Where the drivers should be mounted in the container
    - name: lib
      mountPath: /usr/local/nvidia
```
Mount any required Blob using the FlexVolume driver. As above, this is specified in two parts: (1) what container to mount, and (2) where to mount it in the container.  You can pretty much copy the first part, just change the name of the storage container accordingly. 

```yaml
volumes: # Where the drivers are located on the node
  - name: data
    flexVolume:
      driver: "azure/blobfuse"
      secretRef:
        name: blobfusecreds
      options:
        container: sparkdkakadia # Name of the storage container you want to mount
```
Here we specifty that the volume named ``data`` that we created above, should be mounted as ``/sparkdkakadia`` path in the container. Another way of saying this is programs running on the image can now access any data in the ``sparkdkakadia`` Blob as if it were mounted on the local filesystem at ``/sparkdkakadia``.
```yaml
volumeMounts: # Where the drivers should be mounted in the container
  - name: data
    mountPath: /sparkdkakadia # What path on the container you want it available
```
Here is how the full YAML file would look:

```yaml
apiVersion: batch/v1beta1
kind: CronJob
metadata:
  name: mdl-tf-mnist # Name of your job
spec:
  schedule: "0 * * * *"
  concurrencyPolicy: Replace
  successfulJobsHistoryLimit: 10
  failedJobsHistoryLimit: 3
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: tf-traing
            image: dharmeshkakadia/mdl-tf-mnist
            command: ["python", "mnist_softmax.py"]
            resources:
              limits:
                alpha.kubernetes.io/nvidia-gpu: 1 # How many GPUs you want
            env:
              - name: mnist_data
                value: "/sparkdkakadia/MNIST_data"
            volumeMounts: # Where the drivers should be mounted in the container
            - name: lib
              mountPath: /usr/local/nvidia
            - name: data
              mountPath: /sparkdkakadia # What path on the container you want it available
          restartPolicy: Never
          volumes: # Where the drivers are located on the node
            - name: lib
              hostPath:
                path: /usr/local/nvidia
            - name: data
              flexVolume:
                driver: "azure/blobfuse"
                secretRef:
                  name: blobfusecreds
                options:
                  container: sparkdkakadia # Name of the storage container you want to mount
```

Write a CI/CD VSTS pipeline described on Setup Microservices Infrastructure and CI/CD#ContinuousIntegration(CI).
References:
Example MNIST training pipeline : https://ghe-us.microsoft.com/team-mdl/data-analytics/tree/master/tf-mnist 

References 
