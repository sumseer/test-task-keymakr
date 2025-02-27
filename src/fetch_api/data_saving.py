import pandas as pd

from src.fetch_api.schemas import PostSchema
from src.fetch_api.database.database import get_db
from src.fetch_api.database.models.posts import PostModel


def save_posts_to_csv(posts: list[PostSchema], filename: str = "posts.csv") -> None:
    """Save validated posts to a CSV file."""
    posts_dicts = [post.model_dump() for post in posts]
    df = pd.DataFrame(posts_dicts)

    df.to_csv(filename, index=False, encoding="utf-8")


def save_posts_to_db(posts: list[PostSchema]) -> None:
    """Save validated posts to the SQLite database."""
    db = next(get_db())
    try:
        for post in posts:
            db_post = PostModel(**post.model_dump())
            db.add(db_post)
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Error saving to database: {e}")
    finally:
        db.close()
