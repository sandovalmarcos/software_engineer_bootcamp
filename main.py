from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional

# Crear objeto app
app = FastAPI()

# Clase User, la cual hereda características de BaseModel
class User(BaseModel):

    username: str =Field(
        alias="name",
        title="The Username",
        description="This is the username of the user",
        min_length=1,
        # max_length=20,
        default=None,

    )
    linked_posts: Optional[list[int]] = Field(
        description="Array of post ids the user linked",
        # min_items=2,
        # max_items=10
    )


# Clase que tiene toda la información del usuario
class FullUserProfile(User):
    short_description: str
    long_bio: str


def get_user_info(user_id: str = "default") -> FullUserProfile:
    profile_infos = {
        "default": {
            "short_description": "My bio description",
            "long_bio": "this is our longer bio"
        },
        "user_1": {
            "short_description": "User 1's bio description",
            "long_bio": "User 1's longer bio",
        }
    }

    profile_info = profile_infos[user_id]

    users_content = {
        "default": {
            # "name": "ourusername",
            "link_posts": [1],

            "profile_info": profile_info
        },
        "user_1": {
            "linked_posts": [] * 9,
            "profile_info": profile_info
        }
    }
    user_content = users_content[user_id]
    user = User(**user_content)

    full_user_profile = {
        **profile_info,
        **user.dict()
    }
    return FullUserProfile(**full_user_profile)


def create_user(full_profile_info: FullUserProfile):
    pass


@app.get("/user/me", response_model=FullUserProfile)
def test_endpoint():

    full_user_profile = get_user_info()

    return full_user_profile


@app.get("/user/{user_id}", response_model=FullUserProfile)
def get_user_by_id(user_id: str, company_id: int):
    # print("received user_id: ", user_id, "company_id :", company_id)
    full_user_profile = get_user_info(user_id)

    return full_user_profile
