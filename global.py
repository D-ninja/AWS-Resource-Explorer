import boto3
import pandas as pd


s3_client = boto3.client('s3')
cloudfront_client = boto3.client('cloudfront')


# Function to get S3 buckets
def get_s3_buckets():
    response = s3_client.list_buckets()
    buckets = []
    for bucket in response['Buckets']:
        buckets.append({
            'Region': boto3.session.Session().region_name,
            'Name': bucket['Name']
        })
    return buckets

# Function to get CloudFront distributions
def get_cloudfront_distributions():
    distributions = []
    try:
        response = cloudfront_client.list_distributions()
        if 'DistributionList' in response:
            for distribution in response['DistributionList'].get('Items', []):
                distributions.append({
                    'Region': boto3.session.Session().region_name,
                    'ID': distribution['Id'],
                    'Status':distribution['Status'],
                    'DomainName': distribution['DomainName']
                })
        else:
            print("No CloudFront distributions found.")
    except Exception as e:
        print("An error occurred:", e)
    return distributions


# Function to load existing data from Excel file into dictionary of DataFrames
def load_excel_data(file):
    try:
        with pd.ExcelFile(file) as xls:
            return {sheet_name: xls.parse(sheet_name) for sheet_name in xls.sheet_names}
    except FileNotFoundError:
        return {}

# Combine all resources
s3_buckets = get_s3_buckets()
cloudfront_distributions = get_cloudfront_distributions()

# Convert new data to DataFrames
s3_df = pd.DataFrame(s3_buckets)
cloudfront_df = pd.DataFrame(cloudfront_distributions)



# Load existing data from Excel file
existing_data = load_excel_data('aws_resources.xlsx')

# Append new data to existing DataFrames
existing_data['S3'] = pd.concat([existing_data.get('S3', pd.DataFrame()), s3_df], ignore_index=True)
existing_data['CloudFront'] = pd.concat([existing_data.get('CloudFront', pd.DataFrame()), cloudfront_df], ignore_index=True)


# Write updated DataFrames back to Excel file
with pd.ExcelWriter('aws_resources.xlsx') as writer:
    for sheet_name, df in existing_data.items():
        df.to_excel(writer, sheet_name=sheet_name, index=False)

print("Global Resources information has been appended to 'aws_resources.xlsx' successfully.")
