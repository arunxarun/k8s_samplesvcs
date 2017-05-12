.PHONY: push_image create run_local delete  get_sampleurl

REPO=arunxarun/svc2
TIMESTAMP=tmp-$(shell date +%s )

create:
	@eval $$(minikube docker-env) ;\
  docker image build -t $(REPO):fortest	 -f Dockerfile . ;\
	kubectl create -f k8s_cfg/

run_local:
	cd src; \
	python server.py

push_image:
	@eval $$(minikube docker-env) ;\
	docker image build -t $(REPO):$(TIMESTAMP) -f Dockerfile . ;\
	kubectl set image -f k8s_cfg/svc2_deployment.yaml svc2=$(REPO):$(TIMESTAMP)

get_sampleurl:
	curl http://$(shell minikube ip):$(shell kubectl get service svc2  -o json | jq '.spec.ports[0].nodePort')/resource?value=2;

delete:
	kubectl delete -f k8s_cfg/
