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
