from openai import OpenAI
client = OpenAI()

developer_content = """
You will act as a descriptor of an website. You will response with JSON only with the schema like this.
{
    "tags":["tag1", "tag2"]
    "description":"I am the description of the website."
}
"""

completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "developer",
            "content": developer_content
        },
        {
            "role": "user",
            "content": "https://lakesail.com/"
        }
    ]
)

print(completion.choices[0].message.content)