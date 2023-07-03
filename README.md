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
![lambda-func-overview](https://github.com/bnaikwad88/Automatic-Data-Collection-Storage-Lambda/assets/116859424/441e0439-b284-4406-b968-de0a8b86182a)
![lambda_trigger](https://github.com/bnaikwad88/Automatic-Data-Collection-Storage-Lambda/assets/116859424/7b3c1e41-1933-4493-929b-379aa9e10e6d)


