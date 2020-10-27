# Time Series Forecast using Multi Cloud AI Services

Prafull Porwal, [sp20-516-255](https://github.com/cloudmesh-community/sp20-516-255/blob/main/Cloudmesh-OpenAPI/Readme.md)

* [Contributors](https://github.com/cloudmesh-community/sp20-516-255/graphs/contributors)
* [Insights](https://github.com/cloudmesh-community/fa19-516-147/pulse)
* [Project Code](https://github.com/cloudmesh-community/sp20-516-255/tree/main/Cloudmesh-OpenAPI/AWSForecast)

## Objective

Develop Open API for time series forecasting on multiple clouds

## Introduction

Many cloud providers have introduced machine learning capabilities on their infrastructure. The project aims to provide an open API for timeseries forecasting for AWS using Forecast Services and S3

### AWS AI Service : Forecast Open API Service Features

* Upload the data file to ./cloudmesh/upload-file location
* Upload the json schema file to ./cloudmesh/upload-file location
* Validate the data for missing and less than 0 values
* Split the dataset into Train and test by specifying split percentge.
* Provide list of Multi Cloud supported for Timeseries Forecasting
* Initialize the cloud service
* Create a Dataset Group
* Create a Target Time Series Dataset
* Import data into Forecast from AWS Storage S3
* Create a Predictor
* Generate Forecast
* Query the Forecast

### Additional Features

* Multiple instance of the process supported
* Data Validation and missing values checks


### Environment Configuration

* Python 3.8.2 Python or newer.
* Use a venv (see developer install)
* MongoDB installed as regular program not as service
* AWS boto3 library
* Open API package installed

Make sure that cloudmesh is properly installed on your machine and you have mongodb setup to work with cloudmesh.
More details can be found in the [Cloudmesh Manual](https://cloudmesh.github.io/cloudmesh-manual/installation/install.html)

###  OpenAPI package installation

Make sure you use a python venv before installing. Users can install the code with
```bash
$ pip install cloudmesh-openapi
```

### Pre Requisites :

* add below parameter to cloudmesh.yaml for forecast service to work

    * bucket_name : awsforecastassignnment
    * region_name : us-east-1
    * forecast_srv : forecast
    * forecastquery_srv : forecastquery
    * s3_srv : s3
    * iam_role_arn: XXXXXX
    * algorithmArn: arn:aws:forecast:::algorithm/Deep_AR_Plus

* Data Format : The data should be in csv file format and must have

    * item_id : reference column for which time series forecast is required
    * target_value : the column which need to be predicted, data type integer
    * timestamp : timestamp of data samples

  [AWS Time Series Forecast](https://docs.aws.amazon.com/forecast/latest/dg/API_CreateDataset.html)

* Json Schema : Json Schema file with name schema.json

### Quick Forecast API reference Commands

* Start the open API server for the forecast service
  ```bash
  cms openapi server start .//forecast.yaml
  ```
* Check for supported AI services
  ```bash
  curl http://localhost:8080/cloudmesh/forecast
  ```
  e.g. output:
  "model": "Supported Time Series Forecast Services AWS : Forecast "

* Upload file to the server from location (
  File path should be the location on server where file is located.
  ```bash
  curl "http://localhost:8080/cloudmesh/forecast/upload" -F "upload=@<file_path>\countries-aggregated.csv"
  ```
  e.g. output:
  countries-aggregated.csv uploaded successfully

* Validate data file
  ```bash
  curl "http://localhost:8080/cloudmesh/forecast/validate_data" -F "upload=@<file_path>\countries-aggregated.csv"
  ```
  e.g. output:
  countries-aggregated.csv validated successfully

* Split the data into test and train. Data should be validated first before splitting
  ```bash
  curl http://localhost:8080/cloudmesh/forecast/split_data?split_pct=20
  ```
  output: "Please validate the data first"

  ```bash
  curl http://localhost:8080/cloudmesh/forecast/split_data?split_pct=20
  ```
  output: "Data split successfully"

* Initialize aws parameters
  ```bash
  curl "http://localhost:8080/cloudmesh/forecast/aws"
  ```
  e.g. output:
  {"model":"AWS AI Service initialized successfully"}

* Create Forecast, this is a multistep process, it cretes datasetgroup, dataset, import job, predictor and forecast
  ```bash
  curl http://localhost:8080/cloudmesh/forecast/create_forecast?country=Austrailia
  ```
  This api expects cloud services to be already initialized if not it will request to initialize
  output:

  "Please initialize cloud service"

output: "Forecast generated successfully"

* Lookup a Forecast
```bash
curl http://localhost:8080/cloudmesh/forecast/lookupForecast?countryName=Austrailia
```
output :
shows [ouput](https://github.com/cloudmesh-community/sp20-516-255/blob/main/Cloudmesh-OpenAPI/AWSForecast/sampleOutput)

* Delete Data Stack for the current project
This API should be executed at the end of the session to delete all the resources created for the analysis
```bash
curl "http://localhost:8080/cloudmesh/forecast/deletestack"
```

## Algorithm details

The AWS Forecast service supports following pre-defined algortithms

  * Autoregressive Integrated Moving Average (ARIMA) Algorithm - arn:aws:forecast:::algorithm/ARIMA
  * DeepAR+ Algorithm - arn:aws:forecast:::algorithm/Deep_AR_Plus
  * Exponential Smoothing (ETS) - arn:aws:forecast:::algorithm/ETS
  * Non-Parametric Time Series (NPTS) Algorithm - arn:aws:forecast:::algorithm/NPTS
  * Prophet Algorithm - arn:aws:forecast:::algorithm/Prophet
  * Supports hyperparameter optimization (HPO)

   [AWS Time Series Forecast](https://docs.aws.amazon.com/forecast/latest/dg/forecast.dg.pdf)

## Limitations

  * Requires data file with mandatory colums item_id, target_value and timestamp
  * Requires a schema file schema.json to be provided by the user


## References
https://docs.aws.amazon.com/forecast/latest/dg/forecast.dg.pdf

https://github.com/aws-samples/amazon-forecast-samples
