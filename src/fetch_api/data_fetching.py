import asyncio

import aiohttp
from aiohttp import ClientError, ClientTimeout
from pydantic import ValidationError

from src.fetch_api.exceptions import (
    APIConnectionError,
    APIInvalidURLError,
    APIRequestTimeoutError,
    APIRequestResponseError,
)
# from src.fetch_api.data_saving import save_posts_to_db, save_posts_to_csv
from src.fetch_api.schemas import PostSchema


API_URL = "https://jsonplaceholder.typicode.com/posts"


async def fetch_data(session: aiohttp.ClientSession, url: str) -> list[dict]:
    """Fetch data from the API asynchronously."""
    try:
        async with session.get(url, timeout=ClientTimeout(total=10)) as response:
            if response.status == 200:
                return await response.json()
            raise APIRequestResponseError(status_code=response.status)

    except asyncio.TimeoutError:
        raise APIRequestTimeoutError()
    except ClientError:
        raise APIConnectionError()
    except ValueError:
        raise APIInvalidURLError()


def validate_posts(posts: list[dict]) -> list[PostSchema]:
    """Validate API response using Pydantic."""
    valid_posts = []
    invalid_posts_count = 0

    for post in posts:
        try:
            valid_posts.append(PostSchema.model_validate(post))
        except ValidationError:
            invalid_posts_count += 1

    if invalid_posts_count > 0:
        print(f"Warning! Skipped #{invalid_posts_count} invalid posts.")

    return valid_posts


async def main():
    """Fetch data from API, validate it, and save to database and CSV."""
    connector = aiohttp.TCPConnector(ssl=False)

    async with aiohttp.ClientSession(connector=connector) as session:
        posts = await fetch_data(session, API_URL)
        valid_posts = validate_posts(posts)
        print(valid_posts)


if __name__ == "__main__":
    asyncio.run(main())
