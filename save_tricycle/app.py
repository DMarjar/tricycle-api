import json
from pymysql.cursors import DictCursor
from db_connection import get_db_connection


def lambda_handler(event, __):
    """ This function inserts a new tricycle in the database

    Event:
    ------
    body (dict): The body parameter is a dictionary that contains the following attributes:
        - brand (str): The tricycle brand
        - model (str): The model of the specific tricycle
        - material (str): What the tricycle is made of
        - load_capacity (int): How much the tricycle can carry in kilograms

    Returns
    ------
    dict: A dictionary that contains the status code and a message

    """
    response_headers = {
        'Access-Control-Allow-Headers': '*',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT,DELETE'
    }

    try:
        # Get the body
        body = json.loads(event['body'])

        # Validate payload
        validate_body(body)

        # Insert tricycle
        insert_tricycle(body)

        # Return the tricycles with a 200 status code
        response = {
            'statusCode': 200,
            'headers': response_headers,
            'body': json.dumps("Tricycle " + body['brand'] + " " + body['model'] + " saved successfully")
        }

    except RuntimeError as e:
        response = {
            'statusCode': 500,
            'headers': response_headers,
            'body': json.dumps(f"An error occurred while inserting the tricycle: {str(e)}")
        }

    except ValueError as e:
        response = {
            'statusCode': 400,
            'headers': response_headers,
            'body': json.dumps("A validation error occurred: " + str(e))
        }

    return response


# Validate the body payload
def validate_body(body):
    """ This function validates the body parameter

    Parameters:
    -----------
    body (dict): The body parameter is a dictionary that contains the following attributes:
        - brand (str): The tricycle brand
        - model (str): The model of the specific tricycle
        - material (str): What the tricycle is made of
        - load_capacity (int): How much the tricycle can carry in kilograms

    Raises:
    -------
    ValueError: If the body is not valid
    """
    # Validate if body is not None
    if body is None:
        raise ValueError("Request does not contain a body")

    # Validate required fields in body
    required_fields = ['brand', 'model', 'material', 'load_capacity']
    for field in required_fields:
        if field not in body:
            raise ValueError(f"The {field} attribute is required")
        if body[field] is None:
            raise ValueError(f"The {field} attribute cannot be null")

    # Validate load_capacity type
    if not isinstance(body['load_capacity'], int):
        raise RuntimeError("load_capacity must be an integer")

    # Validate if load_capacity is a positive number
    if body['load_capacity'] < 0:
        raise RuntimeError("load_capacity must be a positive number")


def insert_tricycle(body):
    """ This function inserts a new tricycle in the database """
    connection = get_db_connection()
    try:
        with connection.cursor(DictCursor) as cursor:
            sql = "INSERT INTO tricycle (brand, model, material, load_capacity) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (body['brand'], body['model'], body['material'], body['load_capacity']))
            connection.commit()
    finally:
        connection.close()
