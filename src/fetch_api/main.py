import asyncio

from src.fetch_api.data_fetching import fetch_data, validate_posts
from src.fetch_api.data_saving import save_posts_to_csv, save_posts_to_db
from src.fetch_api.database.settings import init_db

init_db()

API_URL = "https://jsonplaceholder.typicode.com/posts"


async def main():
    """Main function to fetch, validate, and save data."""
    posts = await fetch_data(API_URL)

    valid_posts = validate_posts(posts)

    save_posts_to_csv(valid_posts)
    print("Data saved to posts.csv")

    save_posts_to_db(valid_posts)
    print("Data saved to SQLite database")


if __name__ == "__main__":
    asyncio.run(main())
