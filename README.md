# Designing an Automatic Data Collection and Storage System with AWS Lambda and Slack Integration for Server Availability Monitoring and Slack Notification

## Technologies :
**AWS Lambda, Amazon RDS, CloudWatch, Slack API**

## Objective :
Creating an AWS Lambda function that will periodically fetch data from an API and store it in an Amazon RDS instance. The function should be triggered by an Amazon CloudWatch Event that occurs every 15 seconds(1 minute for Free tier).
To fetch the data from the API, the function should use the requests library (or a similar library) to make a GET request to the API. The function should then use a library such as psycopg2 to connect to the Amazon RDS instance and store the data in the database.
In addition to fetching and storing the data, the function should also use Amazon CloudWatch to monitor the server and send an alert to a Slack community if the server goes down. This can be done using the Slack API.
Overall, the function should be able to run indefinitely and continue to fetch and store the data on a regular basis.

## Approach:
1. Create an AWS Lambda function and configure it to be triggered by an Amazon CloudWatch Event that occurs every 15 seconds/ 1 minute for free tier.
2. In the function's code, use the requests library to make a GET request to the API to fetch the data.
3. Use a library such as psycopg2 to connect to the Amazon RDS instance and store the data in the database.
4. Use Amazon CloudWatch to set up a monitoring alarm that will trigger when the server is unavailable.
5. Use the Slack API to send a message to your Slack community when the alarm is triggered.
6. Test the function to ensure that it is able to fetch and store the data correctly, and that the monitoring and alerting functionality is working as expected.
7. Deploy the function to run indefinitely, continuing to fetch and store the data on a regular basis.

## Expected Results:
The result of the above approach would be an AWS Lambda function that is continuously running and performing the following tasks: 
- Fetching data from an API on a regular basis (every 15 seconds/1 minute).
- Storing the fetched data in an Amazon RDS database.
- Monitoring the server's availability using a CloudWatch Alarm.
- Sending a notification to a Slack channel if the server becomes unavailable.
The function will continue to run and perform these tasks until it is stopped or modified. The Amazon RDS database will contain the data fetched from the API, and the CloudWatch Alarm will be triggered if the server becomes unavailable. The Slack notification will alert users that the server is unavailable, and provide details on the status of the server. The function and the database can be monitored to ensure that they are running and storing data correctly.
# Screenshots of the whole project
### lambda_function.py
```python
import json
import requests
import psycopg2

def lambda_handler(event, context):
    conn = psycopg2.connect(
        host="Your RDS database endpoint",
        user="databse username",
        password="your password"
    )
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS iss_position
                      (id SERIAL PRIMARY KEY,
                       timestamp INTEGER,
                       latitude FLOAT,
                       longitude FLOAT)''')

    try:
        url = "http://api.open-notify.org/iss-now.json"
        response = requests.get(url)
        result = json.loads(response.text)
        timestamp = int(result['timestamp'])
        latitude = float(result['iss_position']['latitude'])
        longitude = float(result['iss_position']['longitude'])

        cursor.execute("INSERT INTO iss_position (timestamp, latitude, longitude) VALUES (%s, %s, %s)",
                       (timestamp, latitude, longitude))
        conn.commit()
    except Exception as e:
        # Handle any exceptions that occur during the execution
        print("An error occurred:", str(e))
        cursor.close()
        conn.close()
        return {
            'statusCode': 500,
            'body': 'An error occurred'
        }
        
    cursor.close()
    conn.close()

    return {
        'statusCode': 200,
        'body': 'Data inserted successfully'
    }

```
### Lambda Function **Position_iss** overview
![lambda-func-overview](https://github.com/bnaikwad88/Automatic-Data-Collection-Storage-Lambda/assets/116859424/441e0439-b284-4406-b968-de0a8b86182a)
### EventsBridge configured trigger
![lambda_trigger](https://github.com/bnaikwad88/Automatic-Data-Collection-Storage-Lambda/assets/116859424/7b3c1e41-1933-4493-929b-379aa9e10e6d)
### RDS available for storage of retrieved data
![RDS_available](https://github.com/bnaikwad88/Automatic-Data-Collection-Storage-Lambda/assets/116859424/c7e78a27-e523-49be-a317-c4406cbcf037)
### lambda_function test-Success
![test_success](https://github.com/bnaikwad88/Automatic-Data-Collection-Storage-Lambda/assets/116859424/00df6932-550d-4844-be55-c2b06c3ef952)
### Overview of pgAdmin with data inserted after every 60 seconds/1 minute
![pg_admin_data_inserted](https://github.com/bnaikwad88/Automatic-Data-Collection-Storage-Lambda/assets/116859424/981d836f-8a9e-4789-b05d-9bd897251d89)
### RDS Stopped
![RDS_unavailable](https://github.com/bnaikwad88/Automatic-Data-Collection-Storage-Lambda/assets/116859424/e0e0dc84-8557-4397-a38e-d07b3b54b544)
### lambda_function test-Success
![test_fail](https://github.com/bnaikwad88/Automatic-Data-Collection-Storage-Lambda/assets/116859424/5d02bea4-093b-4ddc-a1e9-3f40617161d5)
### Cloudwatch Alarm triggered(RDS server down)
![lambda_cloudwatch_alarm](https://github.com/bnaikwad88/Automatic-Data-Collection-Storage-Lambda/assets/116859424/eef38cd8-b8aa-485f-95e9-1e2b58c425ac)
### Gmail-Cloudwatch Alarm triggered
![server-down-cloudwatch-alarm-mail](https://github.com/bnaikwad88/Automatic-Data-Collection-Storage-Lambda/assets/116859424/8c57cc7b-304f-4d7e-a4cc-55520e5c72f3)
### Slack-#lambda-AWS chatbot notification(Server Down)
![server-down-notification-slack](https://github.com/bnaikwad88/Automatic-Data-Collection-Storage-Lambda/assets/116859424/65ed4208-5fed-4625-9983-ae1727bdddb9)
### The alarm stopped after starting the RDS.
![cloudwatch_alarm_resolved](https://github.com/bnaikwad88/Automatic-Data-Collection-Storage-Lambda/assets/116859424/e043f262-6c26-4ced-a26e-63647ac622b0)

# NOTE: Make sure to import packages required for lambda_function are installed in the same Environment on which lambda function is configured.
