import sys
import os
from jinja2 import Template

def main(template_file, handler_file, output_file):
    # Check if the template file exists
    if not os.path.exists(template_file):
        print(f"Error: Template file '{template_file}' not found!")
        sys.exit(1)

    # Check if the handler file exists
    if not os.path.exists(handler_file):
        print(f"Error: Handler file '{handler_file}' not found!")
        sys.exit(1)

    # Load the Jinja2 template
    with open(template_file, 'r') as file:
        template = Template(file.read())

    # Read the content of handler.py
    with open(handler_file, 'r') as file:
        handler_content = file.read()

    # Define the values for the placeholders
    context = {
        'table_name': 'ScoresTable',
        'lambda_role_name': 'LambdaExecutionRole',
        'lambda_function_name': 'ScoreCalculatorFunction',
        'lambda_runtime': 'python3.13',
        'lambda_handler': 'handler.lambda_handler',
        'lambda_code': handler_content
    }

    # Render the template and save to the output file
    with open(output_file, 'w') as file:
        file.write(template.render(context))

    print(f"Template rendered successfully and saved to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python render_template.py <template_file> <handler_file> <output_file>")
        sys.exit(1)

    template_file = sys.argv[1]
    handler_file = sys.argv[2]
    output_file = sys.argv[3]

    main(template_file, handler_file, output_file)