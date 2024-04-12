import boto3
import pandas as pd
import os

# Initialize AWS clients
ec2_client = boto3.client('ec2')
rds_client = boto3.client('rds')
elb_client = boto3.client('elbv2')
autoscaling_client = boto3.client('autoscaling')
lambda_client = boto3.client('lambda')
ecs_client = boto3.client('ecs')
redshift_client = boto3.client('redshift')


# Function to get EC2 instances
def get_ec2_instances():
    response = ec2_client.describe_instances()
    instances = []
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instances.append({
                'Region': boto3.session.Session().region_name,
                'ID': instance['InstanceId'],
                'InstanceType': instance['InstanceType'],
                'State': instance['State']['Name']
            })
    return instances


# Function to get RDS instances
def get_rds_instances():
    response = rds_client.describe_db_instances()
    instances = []
    for db_instance in response['DBInstances']:
        instances.append({
            'Region': boto3.session.Session().region_name,
            'ID': db_instance['DBInstanceIdentifier'],
            'Engine': db_instance['Engine'],
            'Status': db_instance['DBInstanceStatus']
        })
    return instances

# Function to get Load Balancers
def get_load_balancers():
    response = elb_client.describe_load_balancers()
    load_balancers = []
    for lb in response['LoadBalancers']:
        load_balancers.append({
            'Region': boto3.session.Session().region_name,
            'Name': lb['LoadBalancerName'],
            'Type': 'Application' if lb['Type'] == 'application' else 'Network'
        })
    return load_balancers

# Function to get Target Groups
def get_target_groups():
    response = elb_client.describe_target_groups()
    target_groups = []
    for tg in response['TargetGroups']:
        target_groups.append({
            'Region': boto3.session.Session().region_name,
            'Name': tg['TargetGroupName'],
            'Protocol': tg['Protocol'],
            'Port': tg['Port']
        })
    return target_groups

# Function to get Auto Scaling Groups
def get_auto_scaling_groups():
    response = autoscaling_client.describe_auto_scaling_groups()
    auto_scaling_groups = []
    for group in response['AutoScalingGroups']:
        auto_scaling_groups.append({
            'Region': boto3.session.Session().region_name,
            'Name': group['AutoScalingGroupName'],
            'DesiredCapacity': group['DesiredCapacity'],
            'MinSize': group['MinSize'],
            'MaxSize': group['MaxSize']
        })
    return auto_scaling_groups

# Function to get Lambda Functions
def get_lambda_functions():
    response = lambda_client.list_functions()
    lambda_functions = []
    for func in response['Functions']:
        lambda_functions.append({
            'Region': boto3.session.Session().region_name,
            'Name': func['FunctionName'],
            'Runtime': func['Runtime'],
            'MemorySize': func['MemorySize']
        })
    return lambda_functions

# Function to get ECS clusters
def get_ecs_clusters():
    response = ecs_client.list_clusters()
    clusters = []
    for cluster_arn in response['clusterArns']:
        cluster_name = cluster_arn.split('/')[-1]
        clusters.append({
            'Region': boto3.session.Session().region_name,
            'Name': cluster_name
        })
    return clusters

# Function to get Redshift clusters
def get_redshift_clusters():
    response = redshift_client.describe_clusters()
    clusters = []
    for cluster in response['Clusters']:
        clusters.append({
            'Region': boto3.session.Session().region_name,
            'ID': cluster['ClusterIdentifier'],
            'Status': cluster['ClusterStatus']
        })
    return clusters

os.system('export AWS_DEFAULT_REGION=$us-east-1')
# Function to load existing data from Excel file into dictionary of DataFrames
def load_excel_data(file):
    try:
        with pd.ExcelFile(file) as xls:
            return {sheet_name: xls.parse(sheet_name) for sheet_name in xls.sheet_names}
    except FileNotFoundError:
        return {}

# Combine all resources
ec2_instances = get_ec2_instances()
rds_instances = get_rds_instances()
load_balancers = get_load_balancers()
target_groups = get_target_groups()
auto_scaling_groups = get_auto_scaling_groups()
lambda_functions = get_lambda_functions()
ecs_clusters = get_ecs_clusters()
redshift_clusters = get_redshift_clusters()


# Convert new data to DataFrames
ec2_df = pd.DataFrame(ec2_instances)
rds_df = pd.DataFrame(rds_instances)
lb_df = pd.DataFrame(load_balancers)
tg_df = pd.DataFrame(target_groups)
asg_df = pd.DataFrame(auto_scaling_groups)
lambda_df = pd.DataFrame(lambda_functions)
ecs_df = pd.DataFrame(ecs_clusters)
redshift_df = pd.DataFrame(redshift_clusters)

# Load existing data from Excel file
existing_data = load_excel_data('aws_resources.xlsx')

# Append new data to existing DataFrames
existing_data['EC2'] = pd.concat([existing_data.get('EC2', pd.DataFrame()), ec2_df], ignore_index=True)
existing_data['RDS'] = pd.concat([existing_data.get('RDS', pd.DataFrame()), rds_df], ignore_index=True)
existing_data['Load Balancer'] = pd.concat([existing_data.get('Load Balancer', pd.DataFrame()), lb_df], ignore_index=True)
existing_data['Target Groups'] = pd.concat([existing_data.get('Target Groups', pd.DataFrame()), tg_df], ignore_index=True)
existing_data['Auto Scaling Groups'] = pd.concat([existing_data.get('Auto Scaling Groups', pd.DataFrame()), asg_df], ignore_index=True)
existing_data['Lambda Function'] = pd.concat([existing_data.get('Lambda Function', pd.DataFrame()), lambda_df], ignore_index=True)
existing_data['ECS'] = pd.concat([existing_data.get('ECS', pd.DataFrame()), ecs_df], ignore_index=True)
existing_data['Redshift'] = pd.concat([existing_data.get('Redshift', pd.DataFrame()), redshift_df], ignore_index=True)

# Write updated DataFrames back to Excel file
with pd.ExcelWriter('aws_resources.xlsx') as writer:
    for sheet_name, df in existing_data.items():
        df.to_excel(writer, sheet_name=sheet_name, index=False)