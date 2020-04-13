NAME=openapi

all:
	echho "see the targets"

build:
	docker build -t cloudmesh-openapi .

buildclean:
	docker build --no-cache -t cloudmesh-openapi .

#
# TODO: bug there may be other images or non openapi related containers only
#       delete the once from openapi
#
clean:
	docker kill $$(docker ps -q) --force
	docker rm $$(docker ps -a -q) --force
	docker rmi $$(docker images -q) --force

run:
	docker run --rm -t --network="host" --name $(NAME)  -p 8080:8080 $(NAME)

start:
	docker exec -d openapi3 /root/start-server.sh

stop:
	docker exec -d openapi3 /root/stop-server.sh

generate:
	@echo "############################################################"
	@echo "# Need to implements "
	@echo "############################################################"

test:
	@echo "############################################################"
	@echo "# Need to implements "
	@echo "############################################################"

stop:
	docker stop $(NAME)

