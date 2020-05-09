# Test it yourself

## In cloudmesh-openapi

Start server

``` bash
cms openapi server start ./tests/image-analysis/image.yaml
```
Get Response Google Vision

``` bash
curl -sL http://127.0.0.1:8080/cloudmesh/image/detect_text_google
```

Get Response AWS Rekognition

``` bash
curl -sL http://127.0.0.1:8080/cloudmesh/image/detect_text_aws
```

Stop server

``` bash
cms openapi server stop image
```


urls

cloudmesh/image/detect_text_google

cloudmesh/image/detect_text_aws

## image_test.py

How to run test

```bash
pytest -v --capture=no tests/image-analysis/image_test.py 
```

image_test.py has 7 tests

1. Uses generate command to generate new yaml file
2. Check yaml syntax
3. Starts server
4. Does a curl call for google vision api response
5. Does a curl call for aws rekognition api response
6. Stops the server
7. Prints benchmark
