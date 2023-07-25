import json
import boto3
import re
import urllib.parse

print('Loading function')

s3 = boto3.client('s3')

def extract_entities(content):
    # Regular expression to find named entities and capitalized words
    # Regex taken from https://stackoverflow.com/questions/36536495/capitalized-words-with-regular-expression
    pattern = r'(?<!\.\s)(?:\b[A-Z][a-z]+\b) || \b[A-Z][A-Z0-9_]*\b'
    named_entities = re.findall(pattern, content)

    pattern = r'\b[A-Z][A-Z0-9_]*\b'
    capitalized_words = re.findall(pattern, content)

    # Combine both named entities and capitalized words
    entities = named_entities + capitalized_words
    return [entity.strip() for entity in entities if entity.strip()]

def process_content(bucket, key):
    # Get the content of the S3 object
    response = s3.get_object(Bucket=bucket, Key=key)
    content = response['Body'].read().decode('utf-8')

    # Extract entities from the content
    entities = extract_entities(content)

    # Count occurrences of each entity
    all_entities = {}
    for entity in entities:
        all_entities[entity] = all_entities.get(entity, 0) + 1

    return all_entities

def lambda_handler(event, context):
    try:
        # Extract bucket and key from the S3 event
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
        print("Key value : " + str(key))

        # Process content and obtain named entities
        all_entities = process_content(bucket, key)

        # Prepare data in JSON format with modified file name
        data_string = json.dumps({key[-7:-4] + 'ne': all_entities})

        # Save the processed data back to the 'tag-b00945329' S3 bucket
        s3.put_object(
            Bucket='tag-b00945329',
            Key=key.replace('.txt', 'ne.txt'),
            Body=data_string
        )

        # Return the named entities as the Lambda function's result
        return json.dumps(all_entities)

    except Exception as e:
        # Print any exceptions that occur during execution and raise them
        print(e)
        raise e
