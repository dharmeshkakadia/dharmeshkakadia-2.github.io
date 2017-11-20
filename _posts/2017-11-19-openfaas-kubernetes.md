---
published: false
---
## OpenFaaS on Minikube

Minimal steps to run [serveless/functions-as-a-service platform](https://github.com/openfaas) on [Minikube](https://github.com/kubernetes/minikube).

1. Start minikube.
	``minikube start``
2. Install helm, if you haven’t already.
	``brew install kubernetes-helm``
3. Install openfass CLI.
	``brew install faas-cli``
4. Create a new service account for Helm. We are calling it tiller.
	```
	kubectl -n kube-system create sa tiller \
	 && kubectl create clusterrolebinding tiller \
	 — clusterrole cluster-admin \
	 — serviceaccount=kube-system:tiller
    ```
5. Start helm.
	``helm init --skip-refresh --upgrade --service-account tiller``
6. Get openfass kubernetes integration.
	``git clone https://github.com/openfaas/faas-netes && cd faas-netes``
7. Install openfass on Kubernetes.
	``helm upgrade — install --debug --reset-value --set async=false --set rbac=false openfaas openfaas/ ``
	At this point you should see that kubernetes has deployed our serverless infrastructure. 			``kubectl get pods``
    
    ```
    NAME                            READY     STATUS    RESTARTS   AGE
    alertmanager-2526763497-qxzwb   1/1       Running   0          43m
    faas-netesd-1969965387-mtfn3    1/1       Running   0          43m
    gateway-640487255-5k2xr         1/1       Running   0          43m
    hello-4272447001-lkxcs          1/1       Running   0          22m
    prometheus-3793543547-w13ln     1/1       Running   0          43m
    ```
    You can also look at the the ui ``minikube service gateway-external``
	![openfaas.png]({{site.baseurl}}/images/openfaas.png)

  
8. Now, that we have infrastructure, lets build and deploy a python hello world function.
	``faas-cli new --lang python hello``

	This will create ``hello.yml``, ``hello/handler.py`` and ``hello/requirements.txt``. ``hello.yml`` describes the deployment (service name, image to be used etc.). You want to change the image from ``hello`` to ``<your_docker_id>/hello``

	```
    provider:
      name: faas
      gateway: http://localhost:8080
    functions:
      hello:
        lang: python
        handler: ./hello
        image: dharmeshkakadia/hello
    ```

	``hello/handler.py`` has the code to handle request. In our case it just prints back the string.

    ```python
    def handle(st):
        print(st)
    ```
	The requirements file is empty since we don’t have any dependencies right now.

9. Lets build our code, docker image and push it to registry. We will use docker with Kubernetes for this purpose.
	``eval $(minikube docker-env)``
	``docker login``
	``faas-cli build -f hello.yml``
	``faas-cli push -f hello.yml``
    
10. Deploy the hello function service.
	``faas-cli deploy -f hello.yml --gateway $(minikube service gateway-external  --url)``
    At this point you should be seeing the service is deployed
	```
	Deploying: hello.
    No existing function to remove
    Deployed.
    URL: http://192.168.64.4:31112/function/hello
    202 Accepted
    ```
    You can confirm it in UI as well.
    ![hello-openfaas.png]({{site.baseurl}}/images/hello-openfaas.png)


11. You are now ready to test the service. You can invoke it from UI, via REST api or through CLI.
	``echo world | faas-cli invoke hello --gateway $(minikube service gateway-external  --url)``

12. The UI will show the invocation count has changed. You can also confirm it through CLI.
	![hello-deployed-openfaas.png]({{site.baseurl}}/images/hello-deployed-openfaas.png)

	The Prometheus dashboard also has the metrics for the service. Here is the dashboard showing invocation count.
	``minikube service prometheus-external``

	![prometheous-openfaas.png]({{site.baseurl}}/images/prometheous-openfaas.png)

13. Finally you can remove the hello function with
	``faas-cli remove hello --gateway $(minikube service gateway-external  --url)``

	Thats it ! OpenFaaS looks a great platform. Give it a try !
