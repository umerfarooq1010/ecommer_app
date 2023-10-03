from databases import Database

from fastapi import FastAPI,APIRouter, status,Depends,HTTPException,Security

# Importing from project files
from core.database import get_database
from core.models import Product
from core.schemas.schemas import ProductCreateSchema

# Router Object to Create Routes
router = APIRouter(
    prefix='/product',
    tags=["Product"]
)



# ---------------------------------------------------------------------------------------------------

# Creates a single product in product table
@router.post('/create/', status_code=status.HTTP_201_CREATED,
                summary="Create a product",
                response_description="Product created successfully")
async def create_product(record:ProductCreateSchema, database: Database = Depends(get_database)) -> dict:

        """"
            Create a product with following information:

                - **name**: Name of the product. (STR) *--Required*
                - **description**: Description of the product. (STR) *--Required*
                - **product_category_id**: Id of the product_category. (INT) *--Required*

        """

        insert_query = Product.insert().values(record.dict())
        result = await database.execute(insert_query)
        if result is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not created")

        return {'id': result}


#get all products
@router.get('/', status_code=status.HTTP_200_OK,
                summary="Get all products",
                response_description="Products retrieved successfully")
async def get_products(database: Database = Depends(get_database)) -> list:

            """"
                Get all products

            """

            query = Product.select()
            result = await database.fetch_all(query)
            if result is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Products not found")
            return result