# Temperature prediction in Moscow for 24 hours
## Description
The goal of the project:
1) Train a model that will predict the temperature in Moscow for the next 24 hours in 3-hour increments. (8 predictions)
2) Automate the temperature forecasting process based on new data.

# Table of Contents
- [Installation](#installation)
   - [PostgreSQL](#postgresql)
   - [Airflow (ETL + Predict)](#airflow)
- [Project diagram](#project_diagram)
   - [Project Description](#project_description)
- [ETL](#etl-1)
  - [ETL process diagram](#etl_process_diagram)
  - [Description of steps](#etldescription_of_steps)
- [Train_model](#train_model)
   - [Train model process diagram](#train_model_diagram)
   - [Description of steps](#train_model_description)
- [Predict](#predict)
   - [Predict process diagram](#predict_diagram)
   - [Description of steps](#predict_description)
- [Run Process](#run_process)
   - [Airflow (ETL+Predict)](#airflow_run)
   - [Train model (optional)](#train_model_optional)
- [Result](#result)
   - [Example of predictions](#example_of_predictions)

# Installation <a name = "installation"></a>

## PostgreSQL <a name = "postgresql"></a>
Before start process locally, required to create database connection, use next settings (they set as default in project):  
**- Host** - localhost  
**- Database** - postgres  
**- Port** - 5432  
**- Username** - username  
**- Password** - qwerty  

pgAdmin4:
![pgadmin_1](https://github.com/minin2000/Weather-project/assets/65463411/3ed17e7f-28ea-4471-bb70-48a29322c42c)
![pgadmin_2](https://github.com/minin2000/Weather-project/assets/65463411/86e9cc15-9201-4d3e-9af2-60bfe9e604da)

Make sure that you have user - username with Superuser  

![pgadmin_3](https://github.com/minin2000/Weather-project/assets/65463411/64160ea4-f3e7-450e-98da-cea906ab39c1)

Dbeaver:   

![postgresConnectionExample](https://github.com/minin2000/Weather-project/assets/65463411/5f9586ea-fcc7-4597-a53f-6c7e641cfe5d)

## Airflow (ETL + Predict) <a name = "airflow"></a>
For start process locally, follow the steps below:
1) Download folder **Airflow** locally.
   
2) Make sure that docker is running and docker-engine  has sufficient memory allocated.

Before run Airflow, prepare the environment by executing the following steps:
  - If you are working on Linux, specify the AIRFLOW_UID by running the command:

  ```bash
  echo -e "AIRFLOW_UID=$(id -u)" > .env
  ```
  - Perform the database migration and create the initial user account by running the command:

  ```bash
  docker compose up airflow-init
  ```
  The created user account will have the login `airflow` and the password `airflow`.
  
3) Start Airflow and build docker containers:  
```bash
docker compose up --build -d
```



# Project diagram <a name = "project_diagram"></a>

![Project diagram](https://github.com/minin2000/Weather-project/assets/65463411/0bfb5b37-fd95-44af-af21-886c521245f2)

## Project Description <a name = "project_description"></a>

The project consists of the following parts:  

**- ETL** – download historical temperature data in Moscow.   
The data is downloaded from the website https://rp5.ru/Weather_archive_in_Moscow, and then loaded into Postgresql. If a new line is added (new temperature), DAG Predict is launched.

**- Train model** – model training pipeline. Optional part, because the model has already been trained.  

**- Predict** – temperature prediction in Moscow for the next 24 hours. Triggered when a new temperature row is added in the ETL step.  

**Apache Аirflow** is used as an orchestrator.  

**ETL** and **Predict** are loaded as DAGs in Apache Airflow.  

**Train model** is located in a separate folder.  

# ETL <a name = "etl-1"></a>
## ETL process diagram  <a name = "etl_process_diagram"></a>

![ETL drawio](https://github.com/minin2000/temperature-prediction/assets/65463411/0b7a63c5-a3b0-4e2e-bfcc-4921499ecf24)

## Description of steps <a name = "etldescription_of_steps"></a>
**- Init browser** – set options for the driver, indicate the saving path for the downloaded files. Open the browser, return driver.  

**- Download archive** – Go to the website https://rp5.ru/Weather_archive_in_Moscow, enter the weather station - 27612, enter the date range. Download the archive. Returning the path to the archive.  

**- Unzip Archive** – unzip the archive and return the path to the Excel file.  

**- Preprocess data** – We read the excel file and return a dataframe of historical data.  

If there is no 'weather' table in the Database (first run or table deleted) then:  
&nbsp;**- Create db table** – create a table weather. Loading historical data.  

**- Update db table** – Load new data into the ‘weather’ table if there is any.  


# Train model <a name = "train_model"></a>
## Train model process diagram <a name = "train_model_diagram"></a>

![Train model drawio](https://github.com/minin2000/Weather-project/assets/65463411/1aba208c-40e6-42b4-8720-54a542e7fc09)


## Description of steps <a name = "train_model_description"></a>
**- Start** – run docker container or run locally in IDE.  

**- Load raw data** – get the data from the database required for training the model. By default, all rows available in the database are retrieved. To change the data used, CONFIG.py has the fields 'date_from' and 'date_to'. Use them for reproducible experiments. 

**- Preprocess data** – Fill NaN values, create features, create targets (24 hours, 8 columns with 3 hour increments), divide the data into train/val/test.  

**- Tune model** – Optional stage. By default, hyperparameters are already defined in CONFIG.py. If you want to tune hyperparameters yourself, uncomment the part with tune_model. After tunning, the tunned hyperparameters will be used when training the model. 

**- Train model** – train the model, calculate MAE, save the model in the output folder, save training information in mlflow.  

# Predict <a name = "predict"></a>
## Predict process diagram <a name = "predict_diagram"></a>

![Predict drawio](https://github.com/minin2000/Weather-project/assets/65463411/4e4f99c8-cd0b-41e2-ba74-2497895c14df)

## Description of steps <a name = "predict_description"></a>

**- Start** – event based. It is launched after the DAG ETL has completed and a new row with data has been added to the ‘weather’ datatable.

If there is no table 'weather_predictions' in the Database (first run or table deleted) then:  
&nbsp; **- Create db table** – create a ‘weather_predictions’ table.  

**- Load model** – load the trained model.  

**- Load raw data** – get the data from the ‘weather’ datatable, that required to predict the temperature of the next 24 hours.  

**- Preprocess data** – Fill NaN if any, create the dataframe necessary for prediction.  

**- Predict** – predict the weather for the next 24 hours.  

**Postprocess data** – convert prediction results into a dataframe format.  

**Insert to db table** – enter predicted values into the ‘weather_predictions’ datatable.  

# Run Process  <a name = "run_process"></a>
## Airflow (ETL+Predict)  <a name = "airflow_run"></a>
After step 'Installation' is completed, follow for the next steps:  

1) Access the Airflow web interface in your browser at http://localhost:8080.  

2) Login as Username - `airflow`, password - `airflow`

![airflow](https://github.com/minin2000/Weather-project/assets/65463411/c623f969-d8a0-42e5-bce3-d4ce5ee72671)

4) Turn DAG `Weather_ETL`, wait until it finishes. It will create table `weather` in PostgreSQL with historical weather data.
   
![dag weather etl](https://github.com/minin2000/temperature-prediction/assets/65463411/d0c7236b-1df2-4634-9b91-90fc60946bd4)

4) Turn DAG `Weather_prediction`, it will be triggered by `Weather_ETL`. DAG will create table `weather_predictions` where will be predictions for the next 24 hours.

![dag weather prediction](https://github.com/minin2000/Weather-project/assets/65463411/f4fa0631-d63b-4a85-9ae7-7d7ac00dcdf7)


DAG `Weather_ETL` will be triggered every 3 hours and will check if new historical data appeared. If new data appears, `Weather_ETL` will trigger `Weather_prediction` for making new predictions.  

When you are finished working and want to clean up your environment, run:  
 ```bash
 docker compose down --volumes --rmi all
 ```

## Train model (optional)  <a name = "train_model_optional"></a>
If you want to train model, follow next steps:  
1) Download folder **train model** locally  
   
3) In folder create virtual environment:  
   
 ```bash
 python3 -m venv env
 ```
4) Choose created virtual environment:  
```bash
 source env/bin/activate
 ```
5) Install required libs from requirements.txt:  
```bash
 pip install -r requirements.txt
 ```
6) Run mlflow ui:  
```bash
 mlflow ui
 ```
7) Access the MLFlow web interface in your browser at http://127.0.0.1:5000.  
   
8) Uncomment 'params = tune_model(file_dirs, CONFIG)' (Optional, for tunning your model)  

10) Run main.py  

After main.py finishes run, you will find results in MLFlow. Model will be in your-project-folder/output  

![mflow](https://github.com/minin2000/Weather-project/assets/65463411/8e55661a-c46d-482d-8d0b-f921e1e82a3c)


Feel free to create new features in `preprocess_data/feature_engineering`, tune your model, change data to use (`CONFIG['date_from']` `CONFIG['date_to']`)  


# Result <a name = "result"></a>
The following columns were selected as the best columns for weather forecasting, their weights are presented below.
![feature_importance_weight](https://github.com/minin2000/Weather-project/assets/65463411/59a39be0-de0e-4748-8f16-8d4e81bae4e1)


Chosen model: XGBRegressor  
**MAE**: 1.008 (for 8200 test set datetime)  

## Example of predictions <a name = "example_of_predictions"></a>

On a screeshot bellow represents table, where:  
datetime - date and time from which the prediction was made  
temp_X - real temperature after X hours after datetime  
pred_temp_X - predicted temperature afrer X hours after datetime  
MAE_X - error for prediction  
MAE - mean error for all predictions from datetime (8 predictions for each 3 hours)  

![example_table](https://github.com/minin2000/Weather-project/assets/65463411/e1d5c7d3-f9ec-4c02-8a10-2fee2380d8f2)



