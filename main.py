from asyncpg import exceptions
import re
import uvicorn


#import the python packages
from fastapi import FastAPI,status
from fastapi_pagination import add_pagination
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import Response
from fastapi_pagination import add_pagination

#importing the project files
from core.database import get_database
from routers import route
from api_parameters import CORS_ORIGIN_ALL, CORS_ALLOW_METHODS, CORS_ALLOW_HEADERS
from demo_data.import_data import (basic_data_insert)

app = FastAPI()


@app.on_event("startup")
async def startup():
    await get_database().connect()
    await basic_data_insert()

add_pagination(app)
app.include_router(route.router)

# Adding Pagination
add_pagination(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[CORS_ORIGIN_ALL],
    allow_credentials=True,
    allow_methods=[CORS_ALLOW_METHODS],
    allow_headers=[CORS_ALLOW_HEADERS],
)


async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except exceptions.UniqueViolationError as err:
        print(err)
        match = re.search(r'\((.*?)\)', err.detail)
        values = match.group(1)
        column_values = values.split(', ')
        if len(column_values)>1:
            detail = f"{column_values[0].capitalize()} against {column_values[1].lower()} should be unique"
        else:
            detail = err.detail
        response = Response(content=detail, media_type="text/plain")
        response.status_code = status.HTTP_409_CONFLICT
        return response
        # return JSONResponse(status_code=status.HTTP_409_CONFLICT,
        #                     content={'detail':detail})
    except exceptions.ForeignKeyViolationError as err:
        match = re.search(r'\((.*?)\)', err.detail)
        values = match.group(1)
        column_values = values.split(', ')
        response = Response(content=f"{column_values[0].capitalize()} is not present in table {err.table_name.lower()}", media_type="text/plain")
        response.status_code = status.HTTP_409_CONFLICT
        return response


#
app.middleware('http')(catch_exceptions_middleware)
app.include_router(route.router)



@app.on_event("shutdown")
async def shutdown():
    await get_database().disconnect()



if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)



