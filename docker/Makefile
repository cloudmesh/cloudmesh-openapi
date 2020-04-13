clean:
	@echo "############################################################"
	@echo "# Need to implements "
	@echo "############################################################"

build:
	docker build -t openapi3 .

cleanbuild:
	docker build --no-cache -t openapi3 .


dockerclean:
	docker kill $$(docker ps -q) --force
	docker rm $$(docker ps -a -q) --force
	docker rmi $$(docker images -q) --force

run:
	docker run --rm -t --network="host" --name openapi3  -p 8080:8080 openapi3

startservice:
	docker exec -d openapi3 /root/startserver.sh

stopservice:
	docker exec -d openapi3 /root/stopserver.sh

generatorservice:
	@echo "############################################################"
	@echo "# Need to implements "
	@echo "############################################################"

testservice:
	@echo "############################################################"
	@echo "# Need to implements "
	@echo "############################################################"

stop:
	docker stop openapi3

