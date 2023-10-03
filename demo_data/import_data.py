from databases import Database
import pandas as pd
from databases import Database

import os
from sqlalchemy import create_engine, MetaData, Table
from core.database import DATABASE_URL
from core.models import (User,Product,ProductCategory,Inventory,SaleOrder)





async def basic_data_insert():
    try:
        engine = create_engine(DATABASE_URL)
        database = Database(DATABASE_URL)
        if not database.is_connected:
            await database.connect()
        metadata = MetaData(bind=engine)

        await user_table_and_insert_from_csv(engine,database)
        await product_category_table_and_insert_from_csv(engine,database)
        await product_table_and_insert_from_csv(engine,database)
        await inventory_table_and_insert_from_csv(engine,database)
        await sale_order_table_and_insert_from_csv(engine,database)

    except Exception as e:
        print(f"Database connection error: {str(e)}")


async def user_table_and_insert_from_csv(engine,database):
    csv_file_path=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))+"/ecommer_app/demo_data/user_data.csv"
    df = pd.read_csv(csv_file_path)
    select_user_query = User.select()
    user_data_result = await database.fetch_all(select_user_query)
    if len(user_data_result)<1:
        insert_query = User.insert()
        await database.execute_many(query=insert_query, values=df.to_dict(orient='records'))


async def product_category_table_and_insert_from_csv(engine,database):
    csv_file_path=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))+"/ecommer_app/demo_data/product_category.csv"
    df = pd.read_csv(csv_file_path)
    select_product_category_query = ProductCategory.select()
    product_category_data_result = await database.fetch_all(select_product_category_query)
    if len(product_category_data_result)<1:
        # records=df.to_dict(orient='records')
        insert_query = ProductCategory.insert()
        await database.execute_many(query=insert_query, values=df.to_dict(orient='records'))


async def product_table_and_insert_from_csv(engine,database):
    csv_file_path=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))+"/ecommer_app/demo_data/product.csv"
    df = pd.read_csv(csv_file_path)
    select_product_query = Product.select()
    product_data_result = await database.fetch_all(select_product_query)
    if len(product_data_result)<1:
        insert_query = Product.insert()
        await database.execute_many(query=insert_query, values=df.to_dict(orient='records'))



async def inventory_table_and_insert_from_csv(engine,database):
    csv_file_path=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))+"/ecommer_app/demo_data/inventory.csv"
    df = pd.read_csv(csv_file_path)
    select_inventory_query = Inventory.select()
    inventory_data_result = await database.fetch_all(select_inventory_query)
    if len(inventory_data_result)<1:
        insert_query = Inventory.insert()
        await database.execute_many(query=insert_query, values=df.to_dict(orient='records'))








async def sale_order_table_and_insert_from_csv(engine,database):
    csv_file_path=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))+"/ecommer_app/demo_data/sale_order.csv"
    df = pd.read_csv(csv_file_path)
    df['date'] = pd.to_datetime(df['date'])
    select_sale_order_query = SaleOrder.select()
    sale_order_data_result = await database.fetch_all(select_sale_order_query)
    if len(sale_order_data_result)<1:
        insert_query = SaleOrder.insert()
        await database.execute_many(query=insert_query, values=df.to_dict(orient='records'))