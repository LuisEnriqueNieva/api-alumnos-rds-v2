import boto3
import pymysql
import os

def lambda_handler(event, context):
    secret_host = os.environ['DB_HOST']
    user = os.environ['DB_USER']
    secret_password = os.environ['DB_PASSWORD']
    database = os.environ['DB_NAME']

    secrets = boto3.client('secretsmanager')
    host = secrets.get_secret_value(SecretId=secret_host)['SecretString']
    password = secrets.get_secret_value(SecretId=secret_password)['SecretString']

    connection = None
    try:
        connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            db=database,
            connect_timeout=5
        )

        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM alumnos;")
            results = cursor.fetchall()

        return {
            "statusCode": 200,
            "body": results
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "error": str(e)
        }

    finally:
        if connection:
            connection.close()
