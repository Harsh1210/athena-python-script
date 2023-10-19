import boto3

# Configure your AWS credentials and region
aws_access_key_id = ''
aws_secret_access_key = ''
aws_session_token = ''  # Replace with your temporary session token
region_name = 'ap-southeast-1'

# Initialize the Athena client with temporary session credentials
athena = boto3.client('athena', region_name=region_name,
                      aws_access_key_id=aws_access_key_id,
                      aws_secret_access_key=aws_secret_access_key,
                      aws_session_token=aws_session_token)

# Specify the query to run
query = "SELECT * FROM interface_history LIMIT 10"

result_configuration = {'OutputLocation': 's3://vib-km-migration-day-0-bucket/athena-result/'}  # Replace with your S3 bucket and prefix

# Set up the Athena query execution context
query_execution = athena.start_query_execution(
    QueryString=query,
    QueryExecutionContext={
        'Database': 'axe_credit_inter'  # Replace with your database name
    },
    ResultConfiguration=result_configuration
)

# Get the query execution ID
query_execution_id = query_execution['QueryExecutionId']

# Check the query execution status
while True:
    query_execution_status = athena.get_query_execution(
        QueryExecutionId=query_execution_id
    )

    status = query_execution_status['QueryExecution']['Status']['State']
    if status in ['SUCCEEDED', 'FAILED', 'CANCELLED']:
        break

# If the query was successful, fetch the results
if status == 'SUCCEEDED':
    result = athena.get_query_results(QueryExecutionId=query_execution_id)

    # Extract and print the query results
    for row in result['ResultSet']['Rows']:
        for field in row['Data']:
            print(field.get('VarCharValue', ''), end='\t')
        print()
else:
    print(f"Query execution failed with status: {status}")

# Clean up - optional, you can stop query execution here if needed
athena.stop_query_execution(
    QueryExecutionId=query_execution_id
)
