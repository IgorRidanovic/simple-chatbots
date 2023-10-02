#! /usr/bin/env python

# Simple OpenAI command line chatbot. This chatbot uses HTTP requests.
# Igor Ridanovic, www.metafide.com

import requests

# Place your OpenAI API key here
openaiKey = <place your OpenAI key here>


# Setup some basic OpenAI API parameters
endpoint    = 'https://api.openai.com/v1/chat/completions' # The API endpoint
temperature = 0.6                                          # Resonse determinism. 0.0-deterministic, 2.0-random
model       = 'gpt-3.5-turbo'                              # AI model
price       = 0.0015                                       # USD price per 1,000 tokens for this model

# We'll track how much money we spend on API calls.
totalCost = 0


def get_response(chatMsgs):
    # Make a POST HTTP request to OpenAI API.
    headers  = {'Authorization': f'Bearer {openaiKey}'}
    data     = {'model': model, 'temperature': temperature, 'messages': message}
    response = requests.post(endpoint, headers=headers, json=data).json()

    # Parse the information of interest from the OpenAI response.
    answer = response['choices'][0]['message']['content']
    tokens = response['usage']['total_tokens']

    return (answer, tokens)


# Setup few-shot learning.
message = [
            {'role': 'system', 'content': 'You are a helpful assistant and you have a deep knowledge of winter sports.'},
            {'role': 'user',   'content': 'Who is the most decorated alpine skier ever?'},
            {'role': 'system', 'content': 'The most decorated alpine skier ever is Mikaela Shiffrin who in March 2023 defeated the long standing record set by Ingemar Stenmark by winning her 87th FIS World Cup medal.'}
          ]

# Or you can uncomment the following line for a plain assistant chatbot.
# message = [{'role': 'system', 'content': 'You are a helpful assistant.'}]


while True:

    # Get input from CLI.
    prompt = input('Ask me something: ')

    # We always append the past round of conversation with the last response and the
    # new prompt because LLMs have no memory of the past chat.
    message.append({'role': 'user', 'content': prompt})

    # Get response from GPT.
    answer, tokens = get_response(message)

    # Append the answer to the chat.
    message.append({'role': 'assistant', 'content': answer})

    # Get the cost in USD for this API call and add it to the total cost.
    cost = tokens / 1000 * price
    totalCost = totalCost + cost

    # Print to the console. Cost can be very small. Suppres the scientific notation.
    print('-' * 82)
    print(answer)
    print('Cost:', f'{cost:.6f}', 'Total cost for this session:', f'{totalCost:.6f}')
    print()
