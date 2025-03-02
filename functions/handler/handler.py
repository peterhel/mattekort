import math
import boto3
import json
import os
from decimal import Decimal

# Initialize AWS DynamoDB client
dynamodb = boto3.resource('dynamodb')
table_name = os.getenv('DYNAMODB_TABLE', 'ScoresTable')  # Use environment variable or default name
table = dynamodb.Table(table_name)

def calculate_score(success_count, elapsed_seconds):
    """
    Calculate the score based on success_count and elapsed_seconds.
    Uses a logarithmic formula to make the score more exciting.
    Multiplies the score by 100 and converts it to an integer.
    """
    if elapsed_seconds <= 0:
        return 0
    raw_score = success_count / elapsed_seconds
    score = math.log(1 + raw_score) * 100  # Logarithmic scaling
    return int(score * 100)  # Multiply by 100 and convert to integer

def scan_table():
    """
    Scan the DynamoDB table and return items ordered by score in descending order.
    """
    response = table.scan()
    items = response.get('Items', [])
    # Sort items by score in descending order
    sorted_items = sorted(items, key=lambda x: int(x['score']), reverse=True)
    return sorted_items

def lambda_handler(event, context):
    """
    AWS Lambda handler function.
    """
    try:
        http_method = event.get('requestContext').get('http').get('method')  # Default to POST if not specified

        if http_method == 'POST':
            # Handle POST request
            if 'body' in event:
                # Extract the body and parse JSON
                body = json.loads(event['body'])
            else:
                # Assume the event itself is the payload
                body = event

            # Extract parameters from the parsed body
            username = body['username']
            elapsed_seconds = body['elapsed_seconds']
            success_count = body['success_count']

            # Calculate the score
            score = calculate_score(success_count, elapsed_seconds)

            # Prepare the payload to store
            payload = {
                'username': username,
                # 'elapsed_seconds': Decimal(str(elapsed_seconds)),  # Convert to Decimal
                # 'success_count': int(str(success_count)),      # Convert to Decimal
                'score': score                                     # Store as integer
            }

            # Store the payload in DynamoDB
            table.put_item(Item=payload)

            # Get the ordered table scan
            sorted_items = scan_table()

            # Return the response
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({
                    'message': 'Score calculated and stored successfully.',
                    'score': score,
                    'scores': sorted_items
                })
            }

        elif http_method == 'GET':
            # Handle GET request
            sorted_items = scan_table()

            # Return the response
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({
                    'message': 'Scores retrieved successfully.',
                    'scores': sorted_items
                }, default=str)
            }

        else:
            # Unsupported HTTP method
            return {
                'statusCode': 405,
                'headers': {
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({
                    'message': f'HTTP method {http_method} not supported.'
                })
            }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'message': 'An error occurred.',
                'error': str(e)
            })
        }