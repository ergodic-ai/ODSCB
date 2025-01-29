from litellm import completion


def transcribe_image(image_url: str):

    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant. Transcribe the image below.",
        },
        {
            "role": "user",
            "content": [
                {"type": "image_url", "image_url": {"url": image_url}},
            ],
        },
    ]

    results = completion(model="azure/gpt-4o-2", messages=messages)

    return results.choices[0].message.content  # type: ignore


REASONING_FORMAT_PROMPT = """
When dealing with the problem below, you should format your response in the following way:
<think>
[Your step by step reasoning over the problem.]
</think>
Your final response.
"""


def extract_thoughts(response: str) -> str:
    return response.split("<think>")[1].split("</think>")[0]


def extract_response(response: str) -> str:
    return response.split("</think>")[1].strip()


def run(messages, model="azure/gpt-4o-2") -> str:
    prefix_to_system = [
        {
            "role": "system",
            "content": REASONING_FORMAT_PROMPT,
        },
    ]
    if "r1" not in model:
        messages = prefix_to_system + messages
    response = completion(model=model, messages=messages, temperature=0.5)

    if "deepseek-reasoner" in model:
        return (
            "<think>"
            + response.choices[0].message.provider_specific_fields["reasoning_content"]  # type: ignore
            + "</think>\n"
            + response.choices[0].message.content  # type: ignore
        )

    return response.choices[0].message.content  # type: ignore
