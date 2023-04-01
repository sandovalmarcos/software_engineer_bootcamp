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
    liked_posts: Optional[list[int]] = Field(
        description="Array of post ids the user linked",
        # min_items=2,
        # max_items=10
    )


# Clase que tiene toda la información del usuario
class FullUserProfile(User):
    short_description: str
    long_bio: str


class CreateUserResponse(BaseModel):
    user_id: str


profile_infos = {
    0: {
        "short_description": "My bio description",
        "long_bio": "this is our longer bio"
    }
}
users_content = {
    0: {
        # "name": "ourusername",
        "liked_posts": [1] * 9,
    }
}


def get_user_info(user_id: int = 0) -> FullUserProfile:

    profile_info = profile_infos[user_id]

    user_content = users_content[user_id]

    user = User(**user_content)

    full_user_profile = {
        **profile_info,
        **user.dict()
    }
    return FullUserProfile(**full_user_profile)


def create_user(full_profile_info: FullUserProfile) -> int:
    global profile_infos
    global users_content

    new_user_id = len(profile_infos)
    liked_posts = full_profile_info.liked_posts
    short_description = full_profile_info.short_description
    long_bio = full_profile_info.long_bio

    print("before:")
    print("user_content: ", users_content)
    print("profile_info: ", profile_infos)

    users_content[new_user_id] = {"liked_posts": liked_posts}
    profile_infos[new_user_id] = {
        "short_description": short_description,
        "long_bio": long_bio,
    }
    print("after:")
    print("user_content: ", users_content)
    print("profile_info: ", profile_infos)
    return new_user_id


@app.get("/user/me", response_model=FullUserProfile)
def test_endpoint():

    full_user_profile = get_user_info()

    return full_user_profile


@app.get("/user/{user_id}", response_model=FullUserProfile)
def get_user_by_id(user_id: int):
    # print("received user_id: ", user_id, "company_id :", company_id)
    full_user_profile = get_user_info(user_id)

    return full_user_profile


@app.post("/users", response_model=CreateUserResponse)
def add_user(full_profile_info: FullUserProfile):
    user_id = create_user(full_profile_info)
    created_user = CreateUserResponse(user_id=user_id)
    return created_user
