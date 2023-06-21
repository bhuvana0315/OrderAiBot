import openai
from google.cloud import secretmanager

# Create a client
client = secretmanager.SecretManagerServiceClient()

# Specify the name of the secret
secret_name = "projects/569816125116/secrets/Botfastapi/versions/1"

# Access the secret
response = client.access_secret_version(request={"name": secret_name})
api_key = response.payload.data.decode("UTF-8")

# Set the OpenAI API key
openai.api_key = api_key

# Use the OpenAI library
# Rest of your code using the OpenAI library


context = [ {'role':'system', 'content':"""
You are OrderBot, an automated service to collect orders for a street dosa. \
You first greet the customer, then collects the order, \
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
Sprite 10.00,30.00,50.00 \
Thums Up 10.00,30.00,50.00 \
Pepsi 10.00,30.00,50.00 \
Maaza 10.00,30.00,50.00 \
Slice 10.00,30.00,50.00 \


"""} ]  # accumulate messages

# def get_completion_from_message(message, model="gpt-3.5-turbo", temperature=0.5):
#     response = openai.ChatCompletion.create(
#         model=model,
#         messages=[
#             {"role": "system", "content": "You are a helpful assistant."},
#             {"role": "user", "content": message}
#         ],
#         temperature=temperature
#     )
#     return response.choices[0].message.content

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
    context.append({'role':'user', 'content':f"{prompt}"})
    response = get_completion_from_messages(context) 
    context.append({'role':'assistant', 'content':f"{response}"})
    return response