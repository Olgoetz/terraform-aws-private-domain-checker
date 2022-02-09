import requests
import boto3
import logging
import os
import distutils.util

logger = logging.getLogger()
logger.setLevel(logging.ERROR)

cloudwatch = boto3.client('cloudwatch')
lambdah = boto3.client('lambda')



domainname = os.environ['health_check_domain_name']
port = os.environ['port']
path = os.environ['health_check_path']
verify_ssl = os.environ["verify_ssl"]


if verify_ssl == "0":
    _verify_ssl = False
else:
    _verify_ssl = True


def handler(event, context):
    """
    Runs a health check against the provided domain name.If http status code is not 200 - 399 the application is
    most likely not health and an AWS CloudWatch Alarm will be triggered and subscribers to the corresponding
    AWS SNS Topic are notified.

    :param event: AWS event object
    :param context: AWS context object
    :return: none
    """

    url = str("https://" + domainname + ":" + port + "/" + path)

    try:
        internettest = requests.get("https://amazon.com", timeout=2, verify=_verify_ssl)

    except requests.exceptions.ConnectionError as e:
        if "timed out" in str(e):
            print(
                "The Lambda function does not have internet access because it is not in a private subnet with internet access provided by a NAT Gateway or NAT instance. The HTTPS GET request might be successful but Lambda will not be able to push metrics to Cloudwatch and the Route 53 health check will always be unhealthy.")

    try:
        r = requests.get(url, timeout=2, verify=_verify_ssl)
        if r.status_code >= 200 and r.status_code <= 399:
            metric = 1
            print("The HTTPS GET Request to " + domainname + " was successful.")
            print("The HTTPS response code is " + str(r.status_code))
            response = cloudwatch.put_metric_data(Namespace='PrivateHealthCheck', MetricData=[
               {'MetricName': 'HTTPS Health Check for' + domainname,
                'Dimensions': [{'Name': 'HTTPS Health Check', 'Value': 'HTTPS Health Check'}], 'Unit': 'None',
                'Value': metric}, ])


        else:
            metric = 0
            print(
                "The HTTPS GET Request to " + domainname + " was not successful because it received a HTTPS Client Side or Server Side Error Code.")
            print("The HTTPS response code is " + str(r.status_code))
            response = cloudwatch.put_metric_data(Namespace='Route53PrivateHealthCheck', MetricData=[
               {'MetricName':'HTTPS Health Check for' + domainname,
                'Dimensions': [{'Name': 'HTTPS Health Check', 'Value': 'HTTPS Health Check'}], 'Unit': 'None',
                'Value': metric}, ])

    except requests.exceptions.ConnectionError as e:
        metric = 0
        response = cloudwatch.put_metric_data(Namespace='Route53PrivateHealthCheck', MetricData=[
           {'MetricName': 'HTTPS Health Check for' + domainname,
            'Dimensions': [{'Name': 'HTTPS Health Check', 'Value': 'HTTPS Health Check'}], 'Unit': 'None',
            'Value': metric}, ])

        if "Name or service not known" in str(e):
            print(
                "The domain name " + domainname + " does not resolve to an IP address. Kindly ensure the domain name resolves in the VPC.")
        elif "refused" in str(e):
            print(
                "The HTTPS connection was refused by the endpoint. Please check if the endpoint is listening for HTTPS connections on the correct port.")
        elif "timed out" in str(e):
            print(
                "The HTTPS connection timed out because a HTTPS response was not received within the 2 seconds timeout period.")
        elif "SSLError" in str(e):
            print("The HTTPS connection timed out due to SSL error.")
        else:
            logger.error("Error: " + str(e))

    except:
        metric = 0
        response = cloudwatch.put_metric_data(Namespace='Route53PrivateHealthCheck', MetricData=[
           {'MetricName': 'HTTPS Health Check for' + domainname,
            'Dimensions': [{'Name': 'HTTPS Health Check', 'Value': 'HTTPS Health Check'}], 'Unit': 'None',
            'Value': metric}, ])
        logger.error("An error occurred while performing the health check")

