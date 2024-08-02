import json
from pymysql.cursors import DictCursor
from db_connection import get_db_connection


def lambda_handler(__, ___):
    """ This function returns all tricycles in the database

    Returns
    ------
    dict: A dictionary that contains the status code and a list of tricycles or a message if no tricycles are found

    """
    response_headers = {
        'Access-Control-Allow-Headers': '*',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT,DELETE'
    }

    try:
        # Get all tricycles
        tricycles = get_all_tricycles()

        # Validate if there are tricycles, if not return a 204 status code
        if not tricycles:
            response = {
                'statusCode': 204,
                'headers': response_headers,
                'body': json.dumps("No tricycles found")
            }
            return response

        # Return the tricycles with a 200 status code
        response = {
            'statusCode': 200,
            'headers': response_headers,
            'body': json.dumps(tricycles)
        }

    except RuntimeError as e:
        response = {
            'statusCode': 500,
            'headers': response_headers,
            'body': json.dumps(f"An error occurred while getting the tricycles: {str(e)}")
        }

    return response


# Get all tricycles
def get_all_tricycles():
    """ This function gets the tricycles from the database

    Returns:
        list: A list of tricycles
    """
    connection = get_db_connection()
    try:
        with connection.cursor(DictCursor) as cursor:
            sql = "SELECT * FROM tricycle"
            cursor.execute(sql)
            tricycles = cursor.fetchall()
            return tricycles
    finally:
        connection.close()
