import json
import os

import boto3
from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
from botocore.exceptions import ClientError

REGION = 'us-east-1'
HOST = 'search-restaurants-fydg3l6zhn6yhf4sryabkawgfq.us-east-1.es.amazonaws.com'
INDEX = 'restaurants'
queue_url = "https://sqs.us-east-1.amazonaws.com/569179456476/RestaurantQueue"
restaurant_sqs = boto3.client('sqs')
email_ses = boto3.client('ses')
email_sender = "av3162@columbia.edu"


def lambda_handler(event, context):
    response = restaurant_sqs.receive_message(QueueUrl = queue_url, AttributeNames=['All'],MessageAttributeNames=['All'],MaxNumberOfMessages=5,VisibilityTimeout=100,WaitTimeSeconds=20)
    
    if "Messages" not in response:
        return {}
    messages = response["Messages"]
    if len(messages) == 0 :
        return {}
    for message in messages : 
        message_body = json.loads(message["Body"])
        cuisine = message_body["Cuisine"]["value"]["interpretedValue"]
        count = message_body["count"]["value"]["interpretedValue"]
        dining_time = message_body["DiningTime"]["value"]["interpretedValue"]
        date = message_body["Date"]["value"]["interpretedValue"]
        email = message_body["email"]["value"]["interpretedValue"]
        location = message_body["Location"]["value"]["interpretedValue"]
        
        #Elastic search results 
        elastic_results = query(cuisine)
        index = 1
        email_body = f"Hello\nHere are you suggestions for {cuisine} restaurants for {count} people for {date} at {dining_time}.\n"
        for result in elastic_results:
            key = {'id': str(result['Restaurant']), 'cuisine': str(result['cuisine'])}
            restaurant = lookup_data(key)
            email_body = email_body + f"{index}. {restaurant['name']}, located at {restaurant['location']['address1']}\n URL : {restaurant['url']}\n\n"
            index+=1
        
        email_message = {"Subject": {"Data":"Restaurant recommendations"}, "Body":{"Html":{"Data":email_body}}}
        email_ses.send_email(Source = email_sender, Destination = {"ToAddresses":[email]}, Message = email_message)
        restaurant_sqs.delete_message(QueueUrl = queue_url, ReceiptHandle=message['ReceiptHandle'])
    return {
    }


def query(term):
    q = {'size': 5, 'query': {'multi_match': {'query': term}}}

    client = OpenSearch(hosts=[{
        'host': HOST,
        'port': 443
    }],
                        http_auth=get_awsauth(REGION, 'es'),
                        use_ssl=True,
                        verify_certs=True,
                        connection_class=RequestsHttpConnection)

    res = client.search(index=INDEX, body=q)
    print(res)

    hits = res['hits']['hits']
    results = []
    for hit in hits:
        results.append(hit['_source'])

    return results


def get_awsauth(region, service):
    cred = boto3.Session().get_credentials()
    return AWS4Auth(cred.access_key,
                    cred.secret_key,
                    region,
                    service,
                    session_token=cred.token)

def lookup_data(key, db=None, table='RestaurantTable'):
    if not db:
        db = boto3.resource('dynamodb')
    table = db.Table(table)
    try:
        response = table.get_item(Key=key)
    except ClientError as e:
        print('Error', e.response['Error']['Message'])
    else:
        return response['Item']