# Importing FastAPI packages
from fastapi import APIRouter, status,Depends,HTTPException,Security
from databases import Database


# Importing from project files
from core.database import get_database
from core.models import User
from core.schemas.schemas import UserCreateSchema,UserSchema,UserSchemaUpdate
from auth.Token import get_current_user


# Router Object to Create Routes
router = APIRouter(
    prefix='/Users',
    tags=["User"]
)


# ---------------------------------------------------------------------------------------------------


# Creates a single user in user table
@router.post('/signup/', status_code=status.HTTP_201_CREATED,
                summary="Create a user",
                response_description="User created successfully")
async def create_user(record:UserCreateSchema, database: Database = Depends(get_database)) -> dict:

    """"
        Create a user with following information:

            - **first_name**: First name of the user. (STR) *--Required*
            - **last_name**: Last name of the user. (STR) *--Required*
            - **contact**: Contact number of the user. (STR) *--Optional*
            - **email**: Email of the user. (STR) *--Required*
            - **username**: Username of the user. (STR) *--Required*
            - **active**: Active status of the user- *optional*
            - **password**: Password of the user. (STR) *--Required*
            - **company_name**: Company name of the user. (STR) *--Optional*
            - **address**: Address of the user. (STR) *--Optional*
            - **city**: City of the user. (STR) *--Optional*
            - **country**: Country of the user. (STR) *--Optional*
            - **postal_code**: Postal code of the user. (STR) *--Optional*

    """

    insert_query = User.insert().values(record.dict())
    result = await database.execute(insert_query)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not created")

    return {'id': result}

#get single user
@router.get('/{user_id}', status_code=status.HTTP_200_OK,
                summary="Get a single user",
                response_description="User retrieved successfully")
async def get_user(user_id:int, database: Database = Depends(get_database),user=Security(get_current_user)) -> UserSchema:

        """"
            Get a user with following information:

                - **id**: Id of the user. (INT) *--Required*
                - **first_name**: First name of the user. (STR) *--Required*
                - **last_name**: Last name of the user. (STR) *--Required*
                - **contact**: Contact number of the user. (STR) *--Optional*
                - **email**: Email of the user. (STR) *--Required*
                - **username**: Username of the user. (STR) *--Required*
                - **active**: Active status of the user- *optional*
                - **company_name**: Company name of the user. (STR) *--Optional*
                - **address**: Address of the user. (STR) *--Optional*
                - **city**: City of the user. (STR) *--Optional*
                - **country**: Country of the user. (STR) *--Optional*
                - **postal_code**: Postal code of the user. (STR) *--Optional*

        """

        select_query = User.select().where(User.c.id == user_id)
        raw_result = await database.fetch_one(select_query)
        if raw_result is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return UserSchema(**raw_result)


#select all users
@router.get('/', status_code=status.HTTP_200_OK,
                summary="Get all users",
                response_description="Users retrieved successfully")
async def get_all_users(database: Database = Depends(get_database),user=Security(get_current_user)) -> list:

            """"
                Get all users with following information:

                    - **id**: Id of the user. (INT) *--Required*
                    - **first_name**: First name of the user. (STR) *--Required*
                    - **last_name**: Last name of the user. (STR) *--Required*
                    - **contact**: Contact number of the user. (STR) *--Optional*
                    - **email**: Email of the user. (STR) *--Required*
                    - **username**: Username of the user. (STR) *--Required*
                    - **active**: Active status of the user- *optional*
                    - **company_name**: Company name of the user. (STR) *--Optional*
                    - **address**: Address of the user. (STR) *--Optional*
                    - **city**: City of the user. (STR) *--Optional*
                    - **country**: Country of the user. (STR) *--Optional*
                    - **postal_code**: Postal code of the user. (STR) *--Optional*

            """

            select_query = User.select()
            raw_result = await database.fetch_all(select_query)
            if raw_result is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Users not found")
            users= [ UserSchema(**user) for user in raw_result]
            return users

#update user
@router.put('/{user_id}', status_code=status.HTTP_202_ACCEPTED,
                summary="Update a user",
                response_description="User updated successfully")
async def update_user(user_id:int, record:UserSchemaUpdate, database: Database = Depends(get_database),user=Security(get_current_user)) -> dict:

        """"
            Update a user with following information:

                - **id**: Id of the user. (INT) *--Required*
                - **first_name**: First name of the user. (STR) *--Required*
                - **last_name**: Last name of the user. (STR) *--Required*
                - **contact**: Contact number of the user. (STR) *--Required*
                - **active**: Active status of the user- *Required*
                - **company_name**: Company name of the user. (STR) *--Required*
                - **address**: Address of the user. (STR) *--Required*
                - **city**: City of the user. (STR) *--Required*
                - **country**: Country of the user. (STR) *--Required*
                - **postal_code**: Postal code of the user. (STR) *--Required*

        """

        update_query = User.update().returning(User.c.id).where(User.c.id == user_id).values(record.dict())
        result = await database.execute(update_query)
        if result is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not updated")

        return {'id': result}


#delete user
@router.delete('/{user_id}', status_code=status.HTTP_202_ACCEPTED,
                summary="Delete a user",
                response_description="User deleted successfully")
async def delete_user(user_id:int, database: Database = Depends(get_database),user=Security(get_current_user)) -> dict:

            """"
                Delete a user with following information:

                    - **id**: Id of the user. (INT) *--Required*

            """

            delete_query = User.delete().returning(User.c.id).where(User.c.id == user_id)
            result = await database.execute(delete_query)
            if not result:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not deleted")

            return {'id': result, 'message': 'User deleted successfully'}

