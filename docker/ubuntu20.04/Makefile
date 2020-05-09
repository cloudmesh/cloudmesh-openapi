NAME=openapi
IMAGE=cloudmesh-openapi

all:
	echo "see the targets"

build:
	docker build -t $(IMAGE) .

buildclean:
	docker build --no-cache -t $(IMAGE) .

clean:
	docker kill ${NAME}
	docker rm ${NAME}

run:
	docker run --rm -t --network="host" --name $(NAME)  -p 8080:8080 $(IMAGE)

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

