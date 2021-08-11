from sqlalchemy import exc
from starlette.requests import Request
from starlette.responses import Response
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from fastapi.responses import JSONResponse

class AlchemyItemNotFound() : 
    

    async def OnException(request: Request, call_next):
        try:
            return await call_next(request)

        except MultipleResultsFound :
            return JSONResponse(status_code=404, content={"message": "По указанным параметрам найдено больше одного элемента"})

        except NoResultFound:
            return JSONResponse(status_code=404, content={"message": "Элемент с указанными параметрами не найден"})