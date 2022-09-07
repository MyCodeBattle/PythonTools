import requests

files = {
    'format': (None, 'url'),
    'content': (None, f'letitgoyiyuyijhkjhkj'),
    'lexer': (None, '_markdown'),
}

response = requests.post('https://dpaste.org/api/', files=files)

print(response.text)