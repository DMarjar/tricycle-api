import json
from pymysql.cursors import DictCursor
from db_connection import get_db_connection


def lambda_handler(event, __):
    """ This function deletes an existing tricycle from the database

    Event:
    ------
    body (dict): The body parameter is a dictionary that contains the following attributes:
        - id (int): The tricycle id

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

        # Delete tricycle
        delete_tricycle(body)

        # Return the tricycles with a 200 status code
        response = {
            'statusCode': 200,
            'headers': response_headers,
            'body': json.dumps("Tricycle deleted successfully")
        }

    except RuntimeError as e:
        response = {
            'statusCode': 500,
            'headers': response_headers,
            'body': json.dumps(f"An error occurred while deleting the tricycle: {str(e)}")
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
        - id (int): The tricycle id

    Raises:
    -------
    ValueError: If the body is not valid
    """
    # Validate if body is empty
    if body is None:
        raise ValueError("Request does not contain a body")

    # Validate required fields in body
    if 'id' not in body:
        raise ValueError("id is required")

    # Validate id type
    if not isinstance(body['id'], int):
        raise RuntimeError("id must be an integer")

    # Validate if id is a positive number
    if body['id'] < 0:
        raise RuntimeError("id must be a positive number")


# Delete tricycle
def delete_tricycle(body):
    """ This function deletes a new tricycle in the database """
    connection = get_db_connection()
    try:
        with connection.cursor(DictCursor) as cursor:
            sql = "DELETE FROM tricycle WHERE id = %s"
            cursor.execute(sql, (body['id'],))
            if cursor.rowcount == 0:
                raise RuntimeError("Tricycle not found")
            connection.commit()
    finally:
        connection.close()
