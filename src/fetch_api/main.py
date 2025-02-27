import asyncio
import logging

from src.fetch_api.data_fetching import fetch_data, validate_posts
from src.fetch_api.data_saving import save_posts_to_csv, save_posts_to_db
from src.fetch_api.database.settings import init_db

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("api_requests.log"),
        logging.StreamHandler(),
    ],
)

init_db()

API_URL = "https://jsonplaceholder.typicode.com/posts"


async def main():
    """Main function to fetch, validate, and save data."""
    try:
        logging.info(f"Fetching data from API: {API_URL}")
        posts = await fetch_data(API_URL)

        logging.info("Validating fetched data")
        valid_posts = validate_posts(posts)

        logging.info("Saving data to CSV")
        save_posts_to_csv(valid_posts)
        logging.info("Data saved to posts.csv")

        logging.info("Saving data to SQLite database")
        save_posts_to_db(valid_posts)
        logging.info("Data saved to SQLite database")

    except Exception as e:
        logging.error(f"An error occurred: {e}")


if __name__ == "__main__":
    asyncio.run(main())
