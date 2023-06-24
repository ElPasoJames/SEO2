import openai
from flask import render_template, request


API_KEY = ''
openai.api_key = API_KEY
model_id = 'gpt-3.5-turbo-0301'

def chatgpt_conversation(conversation_log):
    response = openai.ChatCompletion.create(
        model=model_id,
        messages=conversation_log
    )

    return response.choices[0].message.content.strip()

    # conversation_log.append({
    #     'role': response.choices[0].message.role,
    #     'content': response.choices[0].message.content.strip()
    # })
    # return conversation_log

def process_gpt(data):
    input1 = data['input1']
    input2 = data['input2']
    # input3 = data['input3']

    question = "Please provide me 5 local Key Words"
    keywords = input1 + " " + input2

    if 'option_2' in data and data['option_2'] == '1':
        question += " also, " + keywords + " and write a local SEO Meta Title 60 characters including spaces."
    if 'option_3' in data and data['option_3'] == '1':
        question += " also, " + keywords + " and write a local SEO Meta Description 100 characters including spaces."
    if 'option_4' in data and data['option_4'] == '1':
        question += " also " + keywords + " and rewrite info for SEO content."
    if 'option_5' in data and data['option_5'] == '1':
        question += " also " + keywords + " and write an SEO Block post using a fun informative sales format."

    conversations = []
    conversations.append({
        'role': 'system',
        # 'content': f'Please read {input1} and {input2} located in city {input3} and write a meta description that is 100 character including spaces'
        'content': question
    })

    result = chatgpt_conversation(conversations)
    result = result.replace('\n', '<br/>')
    print(result)
    return result
    # Open a file to write to
    # with open('output.txt', 'w') as f:
    #     # Write the response from the dashboard.html file to the file
    #     f.write(response.text)

    # while True:
    #     prompt = input('User: ')
    #     result.append({'role': 'user', 'content': prompt})
    #     result = chatgpt_conversation(result)
    #     print()
    #     print('{0}: {1}\n'.format(result[-1]['role'].strip(), result[-1]['content'].strip()))
    #     print(response.text)

    return '{0}: {1}\n'.format(result[-1]['role'].strip(), result[-1]['content'].strip())
