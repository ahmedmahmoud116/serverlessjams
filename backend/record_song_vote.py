import boto3
import os
import json

dynamodb = boto3.client('dynamodb');

def handler(event, context):
    song_name = json.loads(event['body'])['songName'];
    result = dynamodb.update_item(
        TableName = os.environ['DYNAMODB_TABLE'], #Must specify the tablename you are interacting with
        Key = { #help us figure out which item we're trying to reference inside DynamoDB
            'songName':{'S': song_name} #it takes name of attribute and type of value,
                                        #we expect value equal to that coming from the Api Request
        },
        #define how we want to change the value inside of dynamoDB
        #we specify that we want to add in votes attribute inside this item with action increment
        UpdateExpression='ADD votes :inc',
        #then i must define what colon inc is and expattval substitue :inc with the value
        ExpressionAttributeValues={
            ':inc': {'N': '1'}
        },
        ReturnValues="UPDATED_NEW" #It tells us all the new information about the item
    );
    response = {
        "statusCode": 200,
        "headers": {"Access-Control-Allow-Origin": "*"}, #if api available through multiple domains
        "body": json.dumps({"votes": result["Attributes"]["votes"]["N"]})
        #means we want to take from the result operation the attributes.votes.N which is 
        #the count value
    }
    return response;
