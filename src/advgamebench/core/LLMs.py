import anthropic
import openai
import os
from openai import OpenAI
from google import genai
from google.genai import types

def call_chatgpt_41_api(prompt):
    openai.api_key = os.getenv('OPENAI_API_KEY')
    completion = openai.chat.completions.create(
        model="gpt-4.1-2025-04-14",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=2048,
        temperature=0.3,
        top_p=1.0
    )
    return completion.choices[0].message.content

def call_chatgpt_4o_api(prompt):
    openai.api_key = os.getenv('OPENAI_API_KEY')
    completion = openai.chat.completions.create(
        model="gpt-4o-2024-08-06",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=2048,
        temperature=0.3,
        top_p=1.0
    )
    return completion.choices[0].message.content

def call_chatgpt_o3_api(prompt):
    openai.api_key = os.getenv('OPENAI_API_KEY')
    completion = openai.chat.completions.create(
        model="o3-2025-04-16",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return completion.choices[0].message.content

def call_chatgpt_o3_mini_api(prompt):
    openai.api_key = os.getenv('OPENAI_API_KEY')
    completion = openai.chat.completions.create(
        model="o3-mini-2025-01-31",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return completion.choices[0].message.content

def call_deepseek_V3_api(prompt):
    client = OpenAI(api_key=os.getenv('DEEPSEEK_API_KEY'), base_url="https://api.deepseek.com")
    response = client.chat.completions.create(
        model='deepseek-chat',
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": prompt},
        ],
        max_tokens=2048,
        temperature=0.3,
        top_p=1.0
    )
    return response.choices[0].message.content

def call_deepseek_R1_api(prompt):
    client = OpenAI(api_key=os.getenv('DEEPSEEK_API_KEY'), base_url="https://api.deepseek.com")
    response = client.chat.completions.create(
        model='deepseek-reasoner',
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": prompt},
        ],
        max_tokens=2048,
        temperature=0.3,
        top_p=1.0
    )
    return response.choices[0].message.content

def call_qwen_plus_api(prompt):
    client = OpenAI(api_key=os.getenv('QWEN_API_KEY'), base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")
    completion = client.chat.completions.create(
        model="qwen-plus-2025-01-25",
        messages=[
            {'role': 'system', 'content': 'You are a helpful assistant.'},
            {'role': 'user', 'content': prompt}
        ],
        max_tokens=2048,
        temperature=0.3,
        top_p=1.0
    )
    return completion.choices[0].message.content

def call_qwen_max_api(prompt):
    client = OpenAI(api_key=os.getenv('QWEN_API_KEY'), base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")
    completion = client.chat.completions.create(
        model="qwen-max-2025-01-25",
        messages=[
            {'role': 'system', 'content': 'You are a helpful assistant.'},
            {'role': 'user', 'content': prompt}
        ],
        max_tokens=2048,
        temperature=0.3,
        top_p=1.0
    )
    return completion.choices[0].message.content

def call_claude_35_sonnet_api(prompt):
    client = anthropic.Anthropic(api_key=os.getenv('CLAUDE_API_KEY'))
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=2048,
        temperature=0.3,
        top_p=1.0
    )
    return message.content[0].text

def call_gemini_2_flash_api(prompt):
    api_key = os.getenv('GEMINI_API_KEY')
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=prompt,
        config=types.GenerateContentConfig(
            max_output_tokens=2048,
            temperature=0.3,
            top_p=1.0
        )
    )
    return response.text

def call_gemini_2_5_flash_api(prompt):
    api_key = os.getenv('GEMINI_API_KEY')
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.5-flash-preview-04-17",
        contents=prompt,
        config=types.GenerateContentConfig(
            max_output_tokens=2048,
            temperature=0.3,
            top_p=1.0
        )
    )
    return response.text



