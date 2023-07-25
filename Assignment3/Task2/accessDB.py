import boto3
import json


def lambda_handler(event, context):
    try:
        file_name = event["Records"][0]["s3"]["object"]["key"].split('/')[-1]
        bucket_name = "tag-b00945329"
        file_key = "serverless_bucket/" + file_name  # The path to the file in the bucket
        s3_client = boto3.client('s3')

        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('namedEntityTable')

        response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
        file_content = response['Body'].read().decode('utf-8')
        print("file_content : " + str(file_content))
        entity_data = json.loads(file_content)[file_name.replace('.txt', '')]

        print(entity_data)
        for entity, count in entity_data.items():
            item_data = {
                "entity": entity,
                "count": count
            }

            response = table.get_item(Key={'entity': entity})

            if 'Item' in response:
                new_count = response["Item"]["count"] + item_data["count"]
                item_data["count"] = new_count

            table.put_item(Item=item_data)

        return {
            'statusCode': 200,
            'body': str("hello")
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': str(e)
        }
