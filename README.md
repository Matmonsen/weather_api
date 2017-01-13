# Weather api
A Django powered API for fetching weather forecasts.  
Each forecast is cached for 10 minutes.  
The forecast from is fetched from [Yr](http://om.yr.no/verdata/free-weather-data/)

# Installation
0. Have greater or equal version [python 3.5](https://www.python.org/) installed
1. Create folder for project  
  ```
      mkdir weather_api 
  ```  
  ``` 
      cd weather_api
   ```
2. Create virtualenvironment  
  1. With python 2.7  
    ```
        which python3  
    ```  
    ```
        python virtualenv -P with_output_from_which_python3 .
    ```  
  2. With python 3+  
    ```
        python -m venv .
    ```  
3. Activate virtualenv  
  1. Unix systems  
    ```
        source bin/activate
    ```
  2. Windows  
    ```
        Scripts/Activate
    ```  
4. Clone repo  
  ```
      git clone https://github.com/Matmonsen/weather_api
  ```  
5. Install dependencies  
  ```
      cd weather_api
  ```  
  ```
      pip install -r requirements.txt
  ``` 
6. Create local sqlLite3 database  
  ```
      python manage.py migrate
  ```  
6. Start server  
  ```
      python manage.py runserver
  ```
7. [Go to browser at http://127.0.0.1:8000/](http://127.0.0.1:8000/api/search)
8. Specify valid get params  

  [http://127.0.0.1:8000/api/search/?language=en&forecastType=standard&location=spain/catalonia/barcelona](http://127.0.0.1:8000/api/search/?language=en&forecastType=standard&location=spain/catalonia/barcelona)

# Development
1. [Github link to Frontend application in react](https://github.com/Matmonsen/weather_app)
2. [Github link to Yr api wrapper](https://github.com/Matmonsen/py-yr)

# License
See [license](https://github.com/Matmonsen/weather_api/blob/master/LICENSE)
