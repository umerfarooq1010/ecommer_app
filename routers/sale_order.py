from databases import Database
from datetime import date

from fastapi import APIRouter, status,Depends,HTTPException,Security
from fastapi_pagination import Page, paginate
from sqlalchemy import  text,select
from typing import List, Optional, Union, Literal

# Importing from project files
from core.database import get_database
from core.models import SaleOrder,Product
from core.schemas.schemas import SaleOrderSchema


# Router Object to Create Routes
router = APIRouter(
    prefix='/sale_status',
    tags=["Sales Status"]
)



# ---------------------------------------------------------------------------------------------------



#get all sale orders
@router.get('/', status_code=status.HTTP_200_OK,
                summary="Get all sale orders",
                response_model=Page[SaleOrderSchema],
                response_description="Sale orders retrieved successfully")
async def get_sale_orders(database: Database = Depends(get_database)) -> list:

    """"
        Endpoints to retrieve, filter, and analyze sales data with following information:
        - **id**: Id of sale order. (INT) *--Required*
        - **name**: Name of sale order. (STR) *--Required*
        - **description**: Description of sale order. (STR) *--Required*
        - **date**: Date of sale order. (DATE) *--Required*
        - **customer_id**: Customer id of sale order. (INT) *--Required*
        - **product_id**: Product id of sale order. (INT) *--Required*
        - **quantity**: Quantity of sale order. (INT) *--Required*
        - **price**: Price of sale order. (FLOAT) *--Required*
        - **total**: Total of sale order. (FLOAT) *--Required*
    """

    query = SaleOrder.select()
    results = await database.fetch_all(query)
    if results is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sale orders not found")
    data=[SaleOrderSchema(**rec) for rec in results]
    return paginate(data)



# get sale order yearly,monthly,weekly,daily
@router.get('/{period}', status_code=status.HTTP_200_OK,
                summary="Get sale orders by period,period can be yearly,monthly,weekly,daily",
                response_model=Page[dict],
                response_description="Sale orders retrieved successfully")
async def get_sale_orders_by_period(period:Literal['yearly','monthly','weekly','daily'],database: Database = Depends(get_database)) -> list:

        """"
            Endpoints to yearly,monthly,weekly,daily sales data with following information:
            - **year**: Year of sale order. (INT) *--Required*
            - **month**: Month of sale order. (INT) *--Optional*
            - **week**: Week of sale order. (INT) *--Optional*
            - **day**: Day of sale order. (INT) *--Optional*
            - **revenue**: Revenue of sale order. (FLOAT) *--Required*



        """
        if period == 'yearly':
            query= text("""SELECT
                            EXTRACT(YEAR
                        FROM
                            DATE) AS year,
                            SUM(TOTAL) AS revenue
                        FROM
                            SALE_ORDER
                        GROUP BY
                            YEAR
                        """)

            query = query.bindparams()
        elif period == 'monthly':
            query= text("""SELECT
                                EXTRACT(year from DATE) AS year,
                                EXTRACT(MONTH FROM date) AS month,
                            
                                SUM(TOTAL) AS revenue
                            FROM
                                SALE_ORDER
                            GROUP BY
                                year,month
                                """)
        elif period == 'weekly':
            query= text("""
                    SELECT
                        EXTRACT(year from DATE) AS year,
                        EXTRACT(MONTH FROM date) AS month,
                        EXTRACT(WEEK FROM date) AS week, 
                    
                    
                        SUM(TOTAL) AS revenue
                    FROM
                        SALE_ORDER
                    GROUP BY
                        year,month,week""")

        elif period == 'daily':
            query= text("""SELECT
                            EXTRACT(year from DATE) AS year,
                            EXTRACT(MONTH FROM date) AS month,
                            EXTRACT(WEEK FROM date) AS week, 
                            EXTRACT(Day FROM date) AS day, 
                            SUM(TOTAL) AS revenue
                        FROM
                            SALE_ORDER
                        GROUP BY
                            year,month,week,day""")

        query = query.bindparams()
        results = await database.fetch_all(query)
        data=[{**rec} for rec in results]
        return paginate(data)


# get sale order by date range, product id, category id
@router.get('/filter/data/', status_code=status.HTTP_200_OK,
                summary="Get sale orders by date range, product id, category id",
                response_model=Page[SaleOrderSchema],
                response_description="Sale orders retrieved successfully")
async def get_sale_orders_by_filter(start_date:Optional[date]=None,end_date:Optional[date]=None,product_id:Optional[int]=None,category_id:Optional[int]=None,database: Database = Depends(get_database)) -> list:

        """"
            Endpoints to retrieve, filter, and analyze sales data with following information:
            - **id**: Id of sale order. (INT) *--Required*
            - **name**: Name of sale order. (STR) *--Required*
            - **description**: Description of sale order. (STR) *--Required*
            - **date**: Date of sale order. (DATE) *--Required*
            - **customer_id**: Customer id of sale order. (INT) *--Required*
            - **product_id**: Product id of sale order. (INT) *--Required*
            - **quantity**: Quantity of sale order. (INT) *--Required*
            - **price**: Price of sale order. (FLOAT) *--Required*
            - **total**: Total of sale order. (FLOAT) *--Required*
        """

        query = SaleOrder.select()
        if start_date and end_date:
            query = query.where(SaleOrder.c.date.between(start_date, end_date))
        if product_id:
            query = query.where(SaleOrder.c.product_id == product_id)
        if category_id:
            subquery=select([Product.c.id]).where(Product.c.category_id == category_id)
            query = query.where(SaleOrder.c.product_id.in_(subquery))
        results = await database.fetch_all(query)
        if results is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sale orders not found")
        data=[SaleOrderSchema(**rec) for rec in results]
        return paginate(data)