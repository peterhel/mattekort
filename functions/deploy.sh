#!/bin/bash

# Set variables
STACK_NAME="ScoreCalculatorStack"
TEMPLATE_FILE="cf.j2"
GENERATED_FILE="generated.yaml"
HANDLER_FILE="handler.py"

# Check if handler.py exists
if [ ! -f "$HANDLER_FILE" ]; then
  echo "Error: $HANDLER_FILE file not found!"
  exit 1
fi

# Render the Jinja2 template using render_template.py
echo "Rendering the Jinja2 template..."
python3 render_template.py "$TEMPLATE_FILE" "$HANDLER_FILE" "$GENERATED_FILE"
if [ $? -ne 0 ]; then
  echo "Error: Failed to render the template."
  exit 1
fi

# Check if the stack exists
echo "Checking if the stack $STACK_NAME exists..."
STACK_EXISTS=$(aws cloudformation describe-stacks --stack-name $STACK_NAME 2>/dev/null)

if [ $? -eq 0 ]; then
  echo "Stack $STACK_NAME exists. Updating the stack..."
  UPDATE_OUTPUT=$(aws cloudformation update-stack --stack-name $STACK_NAME --template-body file://$GENERATED_FILE --capabilities CAPABILITY_NAMED_IAM 2>&1)

  if echo "$UPDATE_OUTPUT" | grep -q "No updates are to be performed"; then
    echo "No updates to be performed on the stack $STACK_NAME."
  else
    echo "Waiting for the stack update to complete..."
    aws cloudformation wait stack-update-complete --stack-name $STACK_NAME
    echo "Stack $STACK_NAME updated successfully."
  fi
else
  echo "Stack $STACK_NAME does not exist. Creating a new stack..."
  aws cloudformation create-stack --stack-name $STACK_NAME --template-body file://$GENERATED_FILE --capabilities CAPABILITY_NAMED_IAM
  echo "Waiting for the stack creation to complete..."
  aws cloudformation wait stack-create-complete --stack-name $STACK_NAME
  echo "Stack $STACK_NAME created successfully."
fi

# Retrieve and display the outputs
echo "Retrieving stack outputs..."
OUTPUTS=$(aws cloudformation describe-stacks --stack-name $STACK_NAME --query "Stacks[0].Outputs" --output json)

LAMBDA_URL=$(echo $OUTPUTS | jq -r '.[] | select(.OutputKey=="LambdaUrlEndpoint") | .OutputValue')
TABLE_NAME=$(echo $OUTPUTS | jq -r '.[] | select(.OutputKey=="DynamoDBTableName") | .OutputValue')
LAMBDA_NAME=$(echo $OUTPUTS | jq -r '.[] | select(.OutputKey=="LambdaFunctionName") | .OutputValue')

echo "Deployment complete!"
echo "Lambda Function Name: $LAMBDA_NAME"
echo "DynamoDB Table Name: $TABLE_NAME"
echo "Lambda URL Endpoint: $LAMBDA_URL"

# Test the Lambda URL
echo "Testing the Lambda function with a sample payload..."
SAMPLE_PAYLOAD='{"username": "test_user", "elapsed_seconds": 120, "success_count": 30}'
curl -X POST -H "Content-Type: application/json" -d "$SAMPLE_PAYLOAD" $LAMBDA_URL