# k8s_samplesvcs
sample code for k8s workflow presentation

## Purpose
This is some highly contrived code to demonstrate how to develop, debug, deploy, microservice based services and apps in kubernetes. 

### Requirements:
* kubectl: https://kubernetes.io/docs/tasks/kubectl/install/
* minikube: https://kubernetes.io/docs/getting-started-guides/minikube/#installation
* docker toolbox https://www.docker.com/products/docker-toolbox
* make 
* jq: https://stedolan.github.io/jq/download/
* python (I'm running 2.7.10)
* pip: https://packaging.python.org/installing/
* virtualenv: pip install virtualenv


## Demo code
svc1 is a simple service that calls svc2 and returns

```
{ 
    "calling": "http://10.0.0.228:8080/resource", 
    "response": { 
        "service": "SVC2", 
        "value": "value1" 
    }, 
    "service": "SVC1" 
}
```

svc2 is a simple service that returns 

```
{
    "response": {
        "service": "SVC2",
        "value": "2"
    }
}
```

### Makefiles - aka I suck at typing
Makefiles in svc1 and svc2 directories contain the commands I use to deploy, patch, undeploy, demo, and run locally. 
I use kubectl to check status, dump logs, attach to containers, etc. 

### demoing how a pod + service is deployed to minikube

from svc2 subdirectory:
deploy services: `make create` 
  * this calls kubectl to deploy svc1 to match the  service and pod configurations in the k8s_cfg subdir. 
  * note that this runs the following commands:
  ```
  @eval $$(minikube docker-env) ;\   <= this command makes sure container images reside in the image cache on the minikube vm
  docker image build -t $(REPO):latest -f Dockerfile . ;\ <= this command builds the image with the latest timestamp
	kubectl create -f k8s_cfg/  <= this command deploys service and pod
  ```
confirm that service and pod were created:
  * `kubectl get po` - you should see output like this:
  ```
  NAME                    READY     STATUS    RESTARTS   AGE
  svc2-4234125641-xsfs8   1/1       Running   0          1h
  ```
  * `kubectl get svc` - you should see output like this:
  ```
  NAME         CLUSTER-IP   EXTERNAL-IP   PORT(S)          AGE
  kubernetes   10.0.0.1     <none>        443/TCP          5d
  svc1         10.0.0.137   <nodes>       80:31377/TCP     1h
  svc2         10.0.0.228   <nodes>       8080:32318/TCP   2h
  ```
tail  svc2 pod logs: `kubectl logs -f svc2-4234125641-xsfs8`
hit the service: `make get_sampleurl`
  * this command actually interrogates minikube and kubernetes to get the host and IP of the service to hit, then builds a
  curl command. It formats the output from kubectl to json and uses jq to parse that output. 
  ```
  curl http://$(shell minikube ip):$(shell kubectl get service svc2  -o json | jq '.spec.ports[0].nodePort')/resource?value=2;
  ```
  * you should see the payload returned: 
  ```
  {
    "response": {
        "service": "SVC2",
        "value": "2"
    }
  }
  ```
  * you should also see the request in the logs
  
### demoing a service running locally, calling a service in kubernetes
from top level directory:
enter and configure virtual environment: 
* `source venv/bin/activate`
* `pip install requirements.txt`
from svc1 subdirectory:
deploy svc1: `make create`
  * this calls kubectl to deploy svc1 to match the  service and pod configurations in the k8s_cfg subdir. 
run svc1 locally:
  * `make run_local`
  * note that this creates the following environment variables by interrogating minikube and the kubernetes API.
    ```
    export SVC2_SERVICE_HOST=$(shell minikube ip); \
	  export SVC2_SERVICE_PORT=$(shell kubectl get service svc2  -o json | jq '.spec.ports[0].nodePort'); \
    cd src; \
	  python server.py
    ```
  * `curl localhost:8080/resource?value=2` - you should see a response like this:
  ```
  {
    "calling": "http://192.168.99.100:32318/resource",
    "response": {
        "service": "SVC2",
        "value": "value1"
    },
    "service": "SVC1"
  }
  ```
  * cd src
  * change line 59 of server.py from:
  ```
  return {'service': 'SVC1', 'calling': SVC2, 'response': resp['response']}
  ```
  to
  ```
  return {'service': 'SVC1', 'calling': SVC2, 'response': resp['response'],'value': value}
  ```
  * `make push_image` - this command does the following: 
  ```
  @eval $$(minikube docker-env) ;\
	docker image build -t $(REPO):$(TIMESTAMP) -f Dockerfile .   <= build the latest changes
	kubectl set image -f k8s_cfg/svc1_deployment.yaml svc1=$(REPO):$(TIMESTAMP) <= swap out the image in the current deployment
                                                                                 to the one just built
  ```                                                                                
  
  

  

