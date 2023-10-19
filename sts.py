import boto3

# Initialize the STS client
sts = boto3.client('sts')

# Get the caller identity
response = sts.get_caller_identity()

# Extract and print the caller identity information
account_id = response['Account']
user_id = response['UserId']
arn = response['Arn']

print(f"Account ID: {account_id}")
print(f"User ID: {user_id}")
print(f"ARN: {arn}")
