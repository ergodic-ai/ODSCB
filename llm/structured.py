import os
from typing import Any, Generator, Generic, List, Type, TypeVar

import instructor
from litellm import completion
from openai.types.chat import ChatCompletionMessageParam
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

os.environ["LITELLM_LOG"] = "DEBUG"  # 👈 print DEBUG LOGS

client = instructor.from_litellm(completion)

T = TypeVar("T", bound=BaseModel)


def create(messages: List[ChatCompletionMessageParam], response_model: Type[T]) -> T:
    response = client.chat.completions.create(
        model="azure/gpt-4o-2", response_model=response_model, messages=messages
    )
    return response


def create_iterable(
    messages: List[ChatCompletionMessageParam], response_model: Type[T]
) -> Generator[T, None, None]:
    response = client.chat.completions.create_iterable(
        model="azure/gpt-4o-2", response_model=response_model, messages=messages
    )
    return response


class ManyResponseModel(BaseModel, Generic[T]):
    sequence: List[T]


def create_sequence(
    messages: List[ChatCompletionMessageParam], response_model: Type[T]
) -> List[T]:

    response = client.chat.completions.create(
        model="azure/gpt-4o-2", response_model=ManyResponseModel, messages=messages
    )

    return response.sequence


def test_create():
    messages: List[ChatCompletionMessageParam] = [
        {"role": "user", "content": "Extract Jason is 25 years old"}
    ]

    class UserDetail(BaseModel):
        name: str
        age: int

    response = create(messages, UserDetail)
    assert response.name == "Jason"
    assert response.age == 25


if __name__ == "__main__":
    test_create()
