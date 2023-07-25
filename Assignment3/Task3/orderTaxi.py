import json
import random
import boto3


def lambda_handler(event, context):
    # TODO implement
    sns = boto3.client('sns')

    for i in range(3):
        # Lists of car types, accessories, client addresses, and people
        CAR = ["Compact", "Mid-size Sedan", "SUV", "Luxury", "Sports Car", "Convertible"]
        ADDON = ["GPS", "Camera", "Bluetooth Audio", "Sunroof", "Heated Seats", "Premium Sound System"]
        CLIENT = ["1316, 1333 South Park Street", "1102, 1333 South Park Steert", "1332, 3425 Robie Steert"]
        PEOPLE = ["John Smith", "Emily Johnson", "Michael Williams", "Jessica Brown", "David Jones",
                  "Sarah Davis", "Daniel Martinez", "Jennifer Wilson", "Christopher Lee", "Lisa Taylor"]

        # Randomly select car type, accessory, client address, and person
        car_type = random.choice(CAR)
        car_accessories = random.choice(ADDON)
        client_address = random.choice(CLIENT)
        person = random.choice(PEOPLE)

        # Create a booking details message with the selected random information
        booking_details = f"Car Type: {car_type}\nCar Accessory: {car_accessories}\nAddress: {client_address}\nBooked by: {person}"

        # Print the booking details for reference
        print("booking details: " + str(booking_details))

        # Publish the booking details as a message to the 'HalifaxTaxi' SNS topic
        response = sns.publish(
            TopicArn="arn:aws:sns:us-east-1:116244857063:HalifaxTaxi",
            Message=booking_details,
            Subject='New Request for Car'
        )
        # Print the SNS response for reference
        print("SNS response: " + str(response))

    return {
        'statusCode': 200,
        'response': "everything works good",
        'message': "Successful!"
    }
