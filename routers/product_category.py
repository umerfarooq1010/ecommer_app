from databases import Database
from typing import List

from fastapi import APIRouter, status,Depends,HTTPException,Security
from fastapi_pagination import Page, paginate

# Importing from project files
from core.database import get_database
from core.models import ProductCategory
from core.schemas.schemas import ProductCategoryCreateSchema,ProductCategorySchema
from auth.Token import get_current_user

# Router Object to Create Routes
router = APIRouter(
    prefix='/product_category',
    tags=["Product Category"]
)



# ---------------------------------------------------------------------------------------------------

# Creates a single product_category in product_category table
@router.post('/create/', status_code=status.HTTP_201_CREATED,
                summary="Create a product_category",
                response_description="Product_category created successfully")
async def create_product_category(record:ProductCategoryCreateSchema, database: Database = Depends(get_database)) -> dict:

    """"
        Create a product_category with following information:

            - **name**: Name of the product_category. (STR) *--Required*
            - **description**: Description of the product_category. (STR) *--Required*

    """

    insert_query = ProductCategory.insert().values(record.dict())
    result = await database.execute(insert_query)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product Category not created")

    return {'id': result}

#get single product_category
@router.get('/{product_category_id}', status_code=status.HTTP_200_OK,
                summary="Get a single product_category",
                response_description="Product_category retrieved successfully")
async def get_product_category(product_category_id:int, database: Database = Depends(get_database),user=Security(get_current_user)) -> ProductCategorySchema:

    """"
        Get a product_category with following information:

            - **id**: Id of the product_category. (INT) *--Required*

    """

    query = ProductCategory.select().where(ProductCategory.c.id == product_category_id)
    result = await database.fetch_one(query)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product Category not found")
    return ProductCategorySchema(**result)


#get all product_category
@router.get('/', status_code=status.HTTP_200_OK,
                summary="Get all product_category",
                response_model=List[ProductCategorySchema],
                response_description="Product_category retrieved successfully")
async def get_all_product_category(database: Database = Depends(get_database),user=Security(get_current_user)) -> List[ProductCategorySchema]:

    """"
        Get all product_category with following information:

            - **id**: Id of the product_category. (INT) *--Required*


    """

    query = ProductCategory.select()
    result = await database.fetch_all(query)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product Category not found")
    results= [ProductCategorySchema(**rec) for rec in result]
    return results