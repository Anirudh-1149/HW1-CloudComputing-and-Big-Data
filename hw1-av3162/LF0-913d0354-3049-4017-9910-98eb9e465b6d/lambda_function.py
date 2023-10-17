import boto3
import json

# Define the client to interact with Lex
client = boto3.client('lexv2-runtime')

def lambda_handler(event, context):

    # change this to the message that user submits on 
    # your website using the 'event' variable
    msg_from_user = event['messages'][0]

    print(f"Message from frontend: {msg_from_user}")
    user_message_type = msg_from_user['type']
    user_message_text = msg_from_user[user_message_type]['text']

    # Initiate conversation with Lex
    lex_response = client.recognize_text(
            botId='BPCZBCWVLJ', # MODIFY HERE
            botAliasId='B48ORGCNZU', # MODIFY HERE
            localeId='en_US',
            sessionId='testuser',
            text=user_message_text)
    print(f"Lex Message : {lex_response}")
    msg_from_lex = lex_response.get('messages', [])
    response = {
        'messages' : []
    }
    if msg_from_lex:
        print(msg_from_lex)
        lex_messages = []
        for message in msg_from_lex :
            formatted_message = {}
            if message['contentType'] == 'PlainText':
                formatted_message['type'] = 'unstructured'
            formatted_message[formatted_message['type']] = {}
            formatted_message[formatted_message['type']]['text'] = message['content']
            lex_messages.append(formatted_message)
            print(f'formatted_message : {formatted_message}')
        response['messages'] = lex_messages

        # modify resp to send back the next question Lex would ask from the user
        
        # format resp in a way that is understood by the frontend
        # HINT: refer to function insertMessage() in chat.js that you uploaded
        # to the S3 bucket
    else :
        no_message = {}
        no_message['type'] = 'unstructured'
        no_message[no_message['type']] = {}
        no_message[no_message['type']]['text'] = 'No response from lambda'
        response['messages'].append(no_message)
        
        

    return response
