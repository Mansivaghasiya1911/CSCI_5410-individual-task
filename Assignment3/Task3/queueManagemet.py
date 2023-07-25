import json
import boto3

def lambda_handler(event, context):
    # TODO implement

    # Create SQS and SNS clients
    sqsclient = boto3.client("sqs")
    snsclient = boto3.client("sns")

    # Define the URL of the SQS queue
    queueurl = 'https://sqs.us-east-1.amazonaws.com/116244857063/HalifaxTaxiOrder'

    # Receive up to 3 messages from the SQS queue
    response = sqsclient.receive_message(
        QueueUrl=queueurl,
        MaxNumberOfMessages=3
    )
    print("Response value: " + str(response))

    # Check if any messages were received from the SQS queue
    if 'Messages' in response:
        # Process each received message
        for i in range(len(response['Messages'])):
            # Extract the message data as a JSON object
            data = json.loads(response['Messages'][i]['Body'])

            # Publish the extracted message to the 'HalifaxTaxiEmail' SNS topic
            snsclient.publish(
                TopicArn='arn:aws:sns:us-east-1:116244857063:HalifaxTaxiEmail',
                Message=data['Message'],
                Subject=data['Subject'],
                MessageStructure='string'
            )

            # Retrieve the receipt handle for the processed message
            receipt_handle = response['Messages'][i]['ReceiptHandle']
            print(receipt_handle)

            # Delete the processed message from the SQS queue using its receipt handle
            sqsclient.delete_message(
                QueueUrl=queueurl,
                ReceiptHandle=receipt_handle
            )

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
