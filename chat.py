import openai
import os
from dotenv import load_dotenv
import json
from twilio.rest import Client

load_dotenv()

api_key = os.getenv("API_KEY")
openai.api_key = api_key

# Rest of your code using the OpenAI library

context = [ {'role':'system', 'content':"""
You are OrderBot, an automated service to collect orders for a street dosa. \
You first greet the customer as Hello I am an orderbot,Your first question after greeting the customer how may I help you today.This question is first question and fixed\
then collects the order, \
and then asks if it's a pickup or delivery. \
You wait to collect the entire order, then summarize it and check for a final, all amount are in Rupees \
time if the customer wants to add anything else. \
Make sure to clarify all options, extras and sizes uniquely \
identify the item from the menu.\
If it's a delivery, you ask for an address. \
Finally you collect the payment for all the orders.\
Make sure that the payment is made by the customer. \
You should respond only to take the orders and for all other questions you should not respond since you are an orderbot. \
You respond in a short, very conversational friendly style. \
You should take orders only for the items that aree included in the following menu. \
The menu includes \

Masala dosa  40.00 \
Onion dosa   25.00 \
Plain dosa   20.00 \
Ravva dosa   20.00 \
Onion Ravva dosa 30.00 \
Egg dosa 45.00
pesarattu    35.00 \

Drinks: \
bottled water 30.00 \
Tea  
Tea:\
Normal Tea :10.00\
Special Tea: 20.00 \
Ilachi Tea: 15.00\
Green Tea : 15.00 \
Coffee:\
Normal Coffee: 15.00 \
Filtered Coffee: 30.00 \
Black Coffee :20.00\
cool drinks: \
Sprite 10.00,30.00 \
Thums Up 10.00,30.00\
Pepsi 10.00,30.00\
Maaza 10.00,30.00 \
Slice 10.00,30.00 \


"""} ]  # accumulate messages

def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
    )
#   print(str(response.choices[0].message))
    return response.choices[0].message["content"]

def collect_messages_text(msg):
    prompt = msg
    if(prompt=="pickup" or prompt=="delivery"):
        store_order_summary()
    context.append({'role':'user', 'content':f"{prompt}"})
    response = get_completion_from_messages(context) 
    context.append({'role':'assistant', 'content':f"{response}"})
    return response


def store_order_summary():
    context.append({'role':'user','content':'Store the order in a json format with fields containing items,quantity and total price'})
    response = get_completion_from_messages(context) 
    # context.append({'role':'assistant', 'content':f"{response}"})
    print(response)
    with open('order_summary.json', 'w') as json_file:
        json.dump(response, json_file)
    user_phone_number='+916302211930'
    send_whatsapp_message(user_phone_number, response)

def send_whatsapp_message(to, body):
    # Twilio credentials
    twilio_account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    twilio_auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    twilio_whatsapp_number = os.getenv("TWILIO_WHATSAPP_NUMBER")
    # twilio_whatsapp_number = 'whatsapp:+14155238886'  # Twilio's sandbox WhatsApp number

    client = Client(twilio_account_sid, twilio_auth_token)

    try:
        message = client.messages.create(
            from_=twilio_whatsapp_number,
            to='whatsapp:' + to,
            body=body
        )

        print('WhatsApp message sent successfully.')
        print(message.sid)
    except Exception as e:
        print('Error sending WhatsApp message:', str(e))

# import os
# from dotenv import load_dotenv
# from twilio.rest import Client

# load_dotenv()

# # Rest of your code using the OpenAI library

# def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
#     response = openai.ChatCompletion.create(
#         model=model,
#         messages=messages,
#         temperature=temperature,
#     )
#     return response.choices[0].message["content"]


# def send_whatsapp_message(to, body):
#     account_sid = os.getenv("TWILIO_ACCOUNT_SID")
#     auth_token = os.getenv("TWILIO_AUTH_TOKEN")
#     twilio_whatsapp_number = os.getenv("TWILIO_WHATSAPP_NUMBER")

#     client = Client(account_sid, auth_token)

#     try:
#         message = client.messages.create(
#             from_=twilio_whatsapp_number,
#             to='whatsapp:' + to,
#             body=body
#         )

#         print('WhatsApp message sent successfully.')
#         print(message.sid)
#     except Exception as e:
#         print('Error sending WhatsApp message:', str(e))


# # d

# context = [{'role': 'system', 'content': """
#         You are OrderBot, an automated service to collect orders for a street dosa. \
#         Your first question after greeting the customer is, "How may I help you today?" \
#         You collect the order, and then ask if it's a pickup or delivery. \
#         You wait to collect the entire order, then summarize it and check for the final total. \
#         You ask if the customer wants to add anything else. \
#         Make sure to clarify all options, extras, and sizes and uniquely identify the item from the menu. \
#         If it's a delivery, you ask for an address. \
#         Finally, you collect the payment for all the orders. \
#         You should respond only to take orders, and for all other questions, you should not respond since you are an orderbot. \
#         You respond in a short, very conversational, friendly style. \
#         You should take orders only for the items that are included in the following menu. \
#         The menu includes: \

#         Masala dosa  40.00 \
#         Onion dosa   25.00 \
#         Plain dosa   20.00 \
#         Ravva dosa   20.00 \
#         Onion Ravva dosa 30.00 \
#         Egg dosa 45.00 \
#         Pesarattu    35.00 \

#         Drinks: \
#         Bottled water 30.00 \
#         Tea: \
#         Normal Tea : 10.00 \
#         Special Tea: 20.00 \
#         Elachi Tea: 15.00 \
#         Green Tea : 15.00 \
#         Coffee: \
#         Normal Coffee: 15.00 \
#         Filtered Coffee: 30.00 \
#         Black Coffee : 20.00 \
#         Cool drinks: \
#         Sprite 10.00, 30.00, 50.00 \
#         Thums Up 10.00, 30.00, 50.00 \
#         Pepsi 10.00, 30.00, 50.00 \
#         Maaza 10.00, 30.00, 50.00 \
#         Slice 10.00, 30.00, 50.00 \
#         """}]

# def collect_messages_text(msg, user_phone_number=None):
#     # Check if the user provided their phone number in the message
#     if user_phone_number is None:
#         user_phone_number = extract_phone_number_from_message(msg)

#     prompt = msg
#     context.append({'role': 'user', 'content': f"{prompt}"})
#     response = get_completion_from_messages(context)
#     context.append({'role': 'assistant', 'content': f"{response}"})

#     # Send the response as a WhatsApp message
#     if user_phone_number:
#         send_whatsapp_message(user_phone_number, response)

#     return response

# import re

# def extract_phone_number_from_message(msg):
#     # Use regular expression to find a phone number pattern
#     phone_number_pattern = r'\+?\d{1,3}[-.\s]?\(?\d{1,5}\)?[-.\s]?\d{1,5}[-.\s]?\d{1,5}[-.\s]?\d{1,9}'
#     matches = re.findall(phone_number_pattern, msg)

#     # Return the first phone number found, if any
#     if matches:
#         return matches[0]

#     return None
