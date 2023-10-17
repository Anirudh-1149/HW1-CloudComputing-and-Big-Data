import json
from datetime import datetime, timezone, timedelta
from dateutil import tz
import re
import boto3

def validateAddress(address) :
    valid = False
    if "manhattan" in address or ("new" in address and "york" in address) : 
        valid = True
    return valid
    

def validateCuisine(cuisine):
    valid = False
    cuisines = ['chinese', 'italian', 'japanese', 'mediterranean', 'mexican', 'thai']
    if cuisine in cuisines:
        valid = True
    return valid

def validateCount(count):
    valid = False
    if count.isdigit() and int(count) > 0:
        valid = True    
    return valid

def validateDate(date):
    try:
        est = timezone(timedelta(hours=-5))
        visitDate = datetime.strptime(date, '%Y-%m-%d').replace(tzinfo=est).date()
        currentDate = datetime.now(est).date()
        if visitDate < currentDate:
            return False
        return True
    except:
        return False
        
def validateTime(time, date) :
    try:
        est = timezone(timedelta(hours=-5))
        visitDate = datetime.strptime(date, '%Y-%m-%d').replace(tzinfo=est).date()
        currentDate = datetime.now(est).date()
        currentTime = datetime.now(est).time()
        visitTime = datetime.strptime(time, '%H:%M').replace(tzinfo=est).time()
        
        if currentDate == visitDate and currentTime > visitTime:
            return False
        return True
    except: 
        return False

def validateEmail(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if re.match(email_regex, email):
        return True
    else :
        return False

def lambda_handler(event, context):
    print(event)
    bot = event['bot']['name']
    slots = event['sessionState']['intent']['slots']
    intent = event['sessionState']['intent']['name']
    response = {
        "sessionState" :{
            "dialogAction" : {
                "type": "Delegate"
            },
            "intent": {
                'name' : intent,
                'slots': slots
            }
        }
    }
    
    address_response = {
        "sessionState": {
            "dialogAction": {
                "slotToElicit": "Location",
                "type": "ElicitSlot"
            },
            "intent": {
                'name': intent,
                'slots': slots
            }
        },
        "messages": [
            {
                "contentType": "PlainText",
                "content": "Currently suggestions are restricted to manhattan. Which area would you like to eat?"
            }    
        ]
    }
    
    ask_cuisine_response = {
        "sessionState": {
            "dialogAction": {
                "slotToElicit": "Cuisine",
                "type": "ElicitSlot"
            },
            "intent": {
                'name': intent,
                'slots': slots
            }
        },
        "messages": [
            {
                "contentType": "PlainText",
                "content": " What cuisine would you like to try?"
            }    
        ]
    }
    
    invalid_cuisine_response = {
        "sessionState": {
            "dialogAction": {
                "slotToElicit": "Cuisine",
                "type": "ElicitSlot"
            },
            "intent": {
                'name': intent,
                'slots': slots
            }
        },
        "messages": [
            {
                "contentType": "PlainText",
                "content": "Please choose a cuisine among chinese, japanese, mediterranean, mexican and italian."
            }    
        ]
    }
    
    ask_count_response = {
        "sessionState": {
            "dialogAction": {
                "slotToElicit": "count",
                "type": "ElicitSlot"
            },
            "intent": {
                'name': intent,
                'slots': slots
            }
        },
        "messages": [
            {
                "contentType": "PlainText",
                "content": "How many people are in your party?"
            }    
        ]
    }
    
    invalid_count_response = {
        "sessionState": {
            "dialogAction": {
                "slotToElicit": "count",
                "type": "ElicitSlot"
            },
            "intent": {
                'name': intent,
                'slots': slots
            }
        },
        "messages": [
            {
                "contentType": "PlainText",
                "content": "Please provide a valid number."
            }    
        ]
    }
    
    ask_date_response = {
        "sessionState": {
            "dialogAction": {
                "slotToElicit": "Date",
                "type": "ElicitSlot"
            },
            "intent": {
                'name': intent,
                'slots': slots
            }
        },
        "messages": [
            {
                "contentType": "PlainText",
                "content": "When do you plan to visit the restraunt?"
            }    
        ]
    }
    
    invalid_date_response = {
        "sessionState": {
            "dialogAction": {
                "slotToElicit": "Date",
                "type": "ElicitSlot"
            },
            "intent": {
                'name': intent,
                'slots': slots
            }
        },
        "messages": [
            {
                "contentType": "PlainText",
                "content": "Date in the past is not valid. Please provide a valid date."
            }    
        ]
    }
    
    ask_time_response = {
        "sessionState": {
            "dialogAction": {
                "slotToElicit": "DiningTime",
                "type": "ElicitSlot"
            },
            "intent": {
                'name': intent,
                'slots': slots
            }
        },
        "messages": [
            {
                "contentType": "PlainText",
                "content": "At what time will you visit the restraunt?"
            }    
        ]
    }
    
    invalid_time_response = {
        "sessionState": {
            "dialogAction": {
                "slotToElicit": "DiningTime",
                "type": "ElicitSlot"
            },
            "intent": {
                'name': intent,
                'slots': slots
            }
        },
        "messages": [
            {
                "contentType": "PlainText",
                "content": "Time in the past is not valid and please specify the hour of visit."
            }    
        ]
    }
    
    ask_email_response = {
        "sessionState": {
            "dialogAction": {
                "slotToElicit": "email",
                "type": "ElicitSlot"
            },
            "intent": {
                'name': intent,
                'slots': slots
            }
        },
        "messages": [
            {
                "contentType": "PlainText",
                "content": "Lastly, I need your email so I can send you my findings."
            }    
        ]
    }
    
    invalid_email_response = {
        "sessionState": {
            "dialogAction": {
                "slotToElicit": "email",
                "type": "ElicitSlot"
            },
            "intent": {
                'name': intent,
                'slots': slots
            }
        },
        "messages": [
            {
                "contentType": "PlainText",
                "content": "Please enter a valid email"
            }    
        ]
    }
    
    goto_thankyou_intent_response = {
        "sessionState": {
            "dialogAction": {
                "type": "ElicitIntent",
            }
        },
        "messages": [
            {
                "contentType": "PlainText",
                "content": "You’re all set. Expect my suggestions shortly! Have a good day."
            }    
        ]
    }
    
    close_thankyou_intent_response = {
        "sessionState": {
            "dialogAction": {
                "type": "Close",
                "fulfillmentState": "Fulfilled",
                "intent": intent
            }
        },
        "messages": [
            {
                "contentType": "PlainText",
                "content": "Welcome!"
            }    
        ]
    }
    
    #validation input for greeting intent
    if intent == "GreetingIntent" :
        if event['sessionState']['intent']['slots']['action'] :
            response = {
                "sessionState": {
                    "dialogAction": {
                        "type": "ElicitIntent",
                    }
                },
                "messages": [
                    {
                        "contentType": "PlainText",
                        "content": "Great. I can help you with that. What city or city area are you looking to dine in?"
                    }    
                ]
            }
        else :
            response = {
                "sessionState": {
                    "dialogAction": {
                        "slotToElicit": "action",
                        "type": "ElicitSlot"
                    },
                    "intent": {
                        'name': intent,
                        'slots': slots
                    }
                },
                "messages": [
                    {
                        "contentType": "PlainText",
                        "content": "Hi I am Dining Concierge bot. Currently I can help you find restaurants and places to eat."
                    }    
                ]
            }
    elif intent == "DiningSuggestionsIntent" :
        if 'interpretedValue' in event['sessionState']['intent']['slots']['Location']['value'] : 
            #Validate the address data
            address = event['sessionState']['intent']['slots']['Location']['value']['interpretedValue']
            address = address.lower()
            if not validateAddress(address) : 
                return address_response
            elif not event['sessionState']['intent']['slots']['Cuisine']:
                return ask_cuisine_response
        else: 
            return address_response
                
                
        if 'interpretedValue' in event['sessionState']['intent']['slots']['Cuisine']['value'] : 
            #Validate Cuisine Values 
            cuisine = event['sessionState']['intent']['slots']['Cuisine']['value']['interpretedValue']
            cuisine = cuisine.lower()
            if not validateCuisine(cuisine):
                return invalid_cuisine_response
            elif not event['sessionState']['intent']['slots']['count'] :
                return ask_count_response
        else:
            #Ask the question for cuisine
            return invalid_cuisine_response
            
        if 'interpretedValue' in event['sessionState']['intent']['slots']['count']['value'] :
            #Validate the count 
            count = event['sessionState']['intent']['slots']['count']['value']['interpretedValue']
            if not validateCount(count):
                return invalid_count_response
            elif not event['sessionState']['intent']['slots']['Date']: 
                return ask_date_response
        else :
            return invalid_count_response
            
        if 'interpretedValue' in event['sessionState']['intent']['slots']['Date']['value']:
            #Validate the date data
            date = event['sessionState']['intent']['slots']['Date']['value']['interpretedValue']
            if not validateDate(date) :
                return invalid_date_response
            elif not event['sessionState']['intent']['slots']['DiningTime']:
                return ask_time_response
        else:
            #Ask for the date of dining
            return invalid_date_response
        
        if 'interpretedValue' in event['sessionState']['intent']['slots']['DiningTime']['value']:
            time = event['sessionState']['intent']['slots']['DiningTime']['value']['interpretedValue']
            date = event['sessionState']['intent']['slots']['Date']['value']['interpretedValue']
            if not validateTime(time, date):
                return invalid_time_response
            elif not event['sessionState']['intent']['slots']['email']:
                return ask_email_response 
        else :
            return invalid_time_response
            
        if 'interpretedValue' in  event['sessionState']['intent']['slots']['email']['value']:
            #validate the email, push data to Queue service and redirect to ThankYou Intent
            email = event['sessionState']['intent']['slots']['email']['value']['interpretedValue']
            if not validateEmail(email):
                return invalid_email_response
            else :
                sqsClient = boto3.client("sqs")
                response = sqsClient.send_message(
                    QueueUrl="https://sqs.us-east-1.amazonaws.com/569179456476/RestaurantQueue",
                    MessageBody=json.dumps(event['sessionState']['intent']['slots'])
                    )
                return goto_thankyou_intent_response
        else :
            return invalid_email_response
            
    # elif intent == "ThankYouIntent" :
    #     return close_thankyou_intent_response
        
 
    return response
