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
