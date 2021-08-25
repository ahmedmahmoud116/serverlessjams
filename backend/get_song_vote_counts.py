import boto3
import os
import json

dynamodb = boto3.client('dynamodb');

def handler(event, context):
    result = dynamodb.scan(
        TableName = os.environ['DYNAMODB_TABLE'] #Must specify the tablename you are interacting with
    );
    song_votes = [];
    for item in result["Items"]:
        song_votes.append({
            "songName": item["songName"]["S"],
            "votes": item["votes"]["N"]
        }
        )
    response = {
        "statusCode": 200,
        "headers": {"Access-Control-Allow-Origin": "*"}, #if api available through multiple domains
        "body": json.dumps(song_votes)
        #means we want to take from the result operation the attributes.votes.N which is 
        #the count value
    }
    return response;
