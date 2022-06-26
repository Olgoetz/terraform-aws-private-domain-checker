import requests
import boto3
import botocore
import logging
import os


# Setup logger
logger = logging.getLogger()
logger.setLevel(logging.ERROR)

# Initiate clients
cloudwatch_client = boto3.client('cloudwatch')
alb_client = boto3.client("elbv2")

# Parse env variables
domainname = os.environ['health_check_domain_name']
port = os.environ['port']
path = os.environ['health_check_path']
verify_ssl = os.environ["verify_ssl"]
listener_arn = os.environ["listener_arn"]
message_body_502 = os.environ["html_content_502"]
message_body_502 = os.environ["html_content_503"]



# Activate or deactivate SSL
if verify_ssl == "0":
    _verify_ssl = False
else:
    _verify_ssl = True

# Cloudwatch metric data
metric_name = f'HTTPS Health Check for {domainname}'
metric_dimensions = [{'Name': 'HTTPS-Health-Check', 'Value': 'HTTPS Health Check'}]


def create_rule_based_on_priority(listener_arn, message_body, status_code, priority , host_header_value):
    """ Create a listener rule.
    
    :param listener_arn: ARN of the listener
    :param message_body: HTML message body
    :param status_code: HTTP status code
    :param priority: Priority of the rule
    :param host_header_value: FQDN
    :return: none
    """

    try:
        response = alb_client.create_rule(
            ListenerArn=listener_arn,
            Conditions= [{
                'Field': 'host-header',
                'Values': [host_header_value]
            }
            ],
            Priority=priority,
            Actions= [
                {
                    'Type': 'fixed-response',
                    'FixedResponseConfig': {
                        'MessageBody': message_body,
                        'StatusCode': status_code,
                        'ContentType': 'text/html'
                    }
                }
            ]
        )
        print(f"Rule created with prio {priority}, with {status_code} status_code and message_body: {message_body}")
    except botocore.exceptions.ClientError as error:
        logger.error(error)

def delete_rule_based_on_priority(listener_arn, priority):
    """ Delete a listener rule.
    
    :param listener_arn: ARN of the listener
    :param priority: Priority of the rule to delete
    :return: none
    """
    try:
        rules = alb_client.describe_rules(ListenerArn=listener_arn)["Rules"]
      #  print(rules)
        priority_rule_arn = list(filter(lambda rule: rule["Priority"] == str(priority) ,rules))[0]["RuleArn"]
        print(f"Priority {priority} rule ARN: {priority_rule_arn}")
        alb_client.delete_rule(RuleArn=priority_rule_arn)
        print(f"{priority_rule_arn} deleted!")
    except botocore.exceptions.ClientError as error:
        logger.error(error)
    except IndexError as e:
        print(f"No rule with prio {priority} exists")



# Entry point
def handler(event, context):
    """
    Runs a health check against the provided domain name. If http status code is not 200 - 399 the application is
    most likely not healthy and an AWS CloudWatch Alarm will be triggered and subscribers to the corresponding
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
            delete_rule_based_on_priority(listener_arn,str(1))

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
            if r.status_code == 502:
                create_rule_based_on_priority(listener_arn,message_body_502, "502", 1,domainname)

            if r.status_code == 503:
                create_rule_based_on_priority(listener_arn,message_body_503, "503", 1,domainname)
               

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

