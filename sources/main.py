import requests
import boto3
import logging
import os


# Setup logger
logger = logging.getLogger()
logger.setLevel(logging.ERROR)

# Initiate client
cloudwatch_client = boto3.client('cloudwatch')

# Parse env variables
domainname = os.environ['health_check_domain_name']
port = os.environ['port']
path = os.environ['health_check_path']
verify_ssl = os.environ["verify_ssl"]


# Activate or deactivate SSL
if verify_ssl == "0":
    _verify_ssl = False
else:
    _verify_ssl = True

# Cloudwatch metric data
metric_name = f'HTTPS Health Check for {domainname}'
metric_dimensions = [{'Name': 'HTTPS-Health-Check', 'Value': 'HTTPS Health Check'}]


def handler(event, context):
    """
    Runs a health check against the provided domain name.If http status code is not 200 - 399 the application is
    most likely not health and an AWS CloudWatch Alarm will be triggered and subscribers to the corresponding
    AWS SNS Topic are notified.

    :param event: AWS event object
    :param context: AWS context object
    :return: none
    """

    url = f"https://{domainname}:{port}/{path}"

    try:
        r = requests.get(url, timeout=2, verify=_verify_ssl)
        if 200 <= r.status_code <= 399:
            metric = 1
            print(f"The HTTPS GET Request to {domainname} was successful.")
            print(f"The HTTPS response code is {r.status_code}")
            cloudwatch_client.put_metric_data(
                Namespace='PrivateHealthCheck',
                MetricData=[{
                    'MetricName': metric_name,
                    'Dimensions': metric_dimensions,
                    'Value': metric
                },
                ])

        else:
            metric = 0
            print(f"The HTTPS GET Request to {domainname} was not successful because it received a HTTPS Client Side or Server Side Error Code.")
            print(f"The HTTPS response code is {r.status_code}")
            cloudwatch_client.put_metric_data(
                Namespace='PrivateHealthCheck',
                MetricData=[{
                    'MetricName': metric_name,
                    'Dimensions': metric_dimensions,
                    'Value': metric
                },
                ])

    except requests.exceptions.ConnectionError as e:
        metric = 0
        cloudwatch_client.put_metric_data(
            Namespace='PrivateHealthCheck',
            MetricData=[{
                'MetricName': metric_name,
                'Dimensions': metric_dimensions,
                'Value': metric
            },
            ])

        if "Name or service not known" in str(e):
            print(
                f"The domain name {domainname} does not resolve to an IP address. Kindly ensure the domain name resolves in the VPC.")
        elif "refused" in str(e):
            print(
                "The HTTPS connection was refused by the endpoint. Please check if the endpoint is listening for HTTPS connections on the correct port.")
        elif "timed out" in str(e):
            print(
                "The HTTPS connection timed out because a HTTPS response was not received within the 2 seconds timeout period.")
        elif "SSLError" in str(e):
            print("The HTTPS connection timed out due to SSL error.")
        else:
            logger.error(f"Error: {e}")

    except:
        metric = 0
        cloudwatch_client.put_metric_data(
            Namespace='PrivateHealthCheck',
            MetricData=[{
                'MetricName': metric_name,
                'Dimensions': metric_dimensions,
                'Value': metric
            },
            ])
        logger.error("An error occurred while performing the health check")

    return "Lambda finished!"

