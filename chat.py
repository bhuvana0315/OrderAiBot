import openai

openai.api_key = ""

def get_completion_from_message(message, model="davinci", temperature=0.5):
    response = openai.Completion.create(
        engine=model,
        prompt=message,
        temperature=temperature,
        max_tokens=50,
        n=1,
        stop=None
    )
    return response.choices[0].text
