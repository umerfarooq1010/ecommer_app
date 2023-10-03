from databases import Database

from fastapi import APIRouter, status,Depends,HTTPException,Security
from fastapi_pagination import Page, paginate
# Importing from project files
from core.database import get_database
from core.models import Inventory
from core.schemas.schemas import InventorySchema,InventorySchemaPatch
from auth.Token import get_current_user


# Router Object to Create Routes
router = APIRouter(
    prefix='/inventory_management',
    tags=["Inventory Management"]
)


# ---------------------------------------------------------------------------------------------------

#get all inventory
@router.get('/', status_code=status.HTTP_200_OK,
                summary="Get all inventory",
                response_model=Page[InventorySchema],
                response_description="Inventory retrieved successfully")
async def get_inventory(database: Database = Depends(get_database)) -> dict:
    """
        Endpoints to retrieve, filter, and analyze inventory data with following information:
        - **id**: Id of inventory. (INT) *--Required*
        - **product_id**: Product id of inventory. (INT) *--Required*
        - **quantity**: Quantity of inventory. (INT) *--Required*
        - **threshold**: Threshold of inventory. (INT) *--Required*
        - **alert**: Alert of inventory. (BOOL) *--Required*
        - **created_by**: Created by of inventory. (INT) *--Required*
        - **updated_by**: Updated by of inventory. (INT) *--Required*
        - **created_at**: Created at of inventory. (DATE) *--Required*
        - **updated_at**: Updated at of inventory. (DATE) *--Required*

    """
    query = Inventory.select()
    results = await database.fetch_all(query)
    if results is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inventory not found")
    data=[InventorySchema(**rec) for rec in results]
    return paginate(data)



#patch inventory
@router.patch('/{id}', status_code=status.HTTP_200_OK,
                summary="Update inventory",
                response_model=dict,
                response_description="Inventory updated successfully")
async def update_inventory(id:int,record:InventorySchemaPatch,
                           database: Database = Depends(get_database),current_user: dict = Security(get_current_user, scopes=["admin"])) -> dict:
    """
        Endpoints to update inventory data with following information:
        - **quantity**: Quantity of inventory. (INT) *--Required*
        - **threshold**: Threshold of inventory. (INT) *--Required*

    """
    data =record.dict(exclude_unset=True)
    data['updated_by']=current_user['id']
    query = Inventory.update().returning(Inventory.c.id).where(Inventory.c.id==id).values(data)
    update_inventory_id=await database.execute(query)
    if update_inventory_id:
        query=Inventory.select().where(Inventory.c.id==update_inventory_id)
        updated_data=await database.fetch_one(query)
        return dict(updated_data)

    raise  HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inventory not found")




