.PHONY: push_image create run_local delete  get_service

REPO=arunxarun/svc1
TIMESTAMP=tmp-$(shell date +%s )

create:
	@eval $$(minikube docker-env) ;\
	docker image build -t $(REPO):fortest -f Dockerfile . ;\
	kubectl create -f k8s_cfg/

run_local:
	export SVC2_SERVICE_HOST=$(shell minikube ip); \
	export SVC2_SERVICE_PORT=$(shell kubectl get service svc2  -o json | jq '.spec.ports[0].nodePort'); \
  cd src; \
	python server.py

run_tests:
	export SVC2_SERVICE_HOST=$(shell minikube ip); \
	export SVC2_SERVICE_PORT=$(shell kubectl get service svc2  -o json | jq '.spec.ports[0].nodePort'); \
  pytest test/*
	
push_image:
	@eval $$(minikube docker-env) ;\
	docker image build -t $(REPO):$(TIMESTAMP) -f Dockerfile .
	kubectl set image -f k8s_cfg/svc1_deployment.yaml svc1=$(REPO):$(TIMESTAMP)

get_sampleurl:
		curl http://$(shell minikube ip):$(shell kubectl get service svc1  -o json | jq '.spec.ports[0].nodePort')/resource?value=2;

delete:
	kubectl delete -f k8s_cfg/
