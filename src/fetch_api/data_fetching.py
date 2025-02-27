import asyncio
import logging

import aiohttp
from aiohttp import ClientError, ClientTimeout
from pydantic import ValidationError

from src.fetch_api.exceptions import (
    APIConnectionError,
    APIInvalidURLError,
    APIRequestTimeoutError,
    APIRequestResponseError,
)
from src.fetch_api.schemas import PostSchema


async def fetch_data(url: str) -> list[dict]:
    """Fetch data from the API asynchronously."""
    connector = aiohttp.TCPConnector(ssl=False)

    async with aiohttp.ClientSession(connector=connector) as session:
        try:
            logging.info(f"Making request to: {url}")
            async with session.get(url, timeout=ClientTimeout(total=10)) as response:
                logging.info(f"Received response with status: {response.status}")
                if response.status == 200:
                    return await response.json()
                raise APIRequestResponseError(status_code=response.status)

        except asyncio.TimeoutError:
            logging.error("Request timed out")
            raise APIRequestTimeoutError()
        except ClientError as e:
            logging.error(f"Client error occurred: {e}")
            raise APIConnectionError()
        except ValueError as e:
            logging.error(f"Invalid URL: {e}")
            raise APIInvalidURLError()


def validate_posts(posts: list[dict]) -> list[PostSchema]:
    """Validate API response using Pydantic."""
    valid_posts = []
    invalid_posts_count = 0

    for post in posts:
        try:
            valid_posts.append(PostSchema.model_validate(post))
        except ValidationError as e:
            invalid_posts_count += 1
            logging.warning(f"Validation error for post: {post}. Error: {e}")

    if invalid_posts_count > 0:
        logging.warning(f"Skipped {invalid_posts_count} invalid posts.")

    return valid_posts
