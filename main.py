from typing import List, Union
from fastapi import FastAPI, UploadFile, Query, File
from database import generateConection
from schemas import AuditResponse, FileResponse
from utils import buildQuery, csvToJson, pickFields, parseDate, parseResponse
from starlette.exceptions import HTTPException
from datetime import date
from pydantic import Field
import pymongo

app = FastAPI()
db = generateConection()
collection = db.get_collection("audits")

# index creation
collection.create_index([("createdDate", pymongo.DESCENDING)],
    background=True)
collection.create_index([("modifiedDate", pymongo.DESCENDING)],
    background=True)

DEFAUTL_FIELDS = ["transactionId",
    "workflowId",
    "userId",
    "clientId",
    "action",
    "prevValue",
    "currentValue"]

FILE_TYPES = ["application/csv", "text/csv"]

@app.post("/file", description="Load a csv file into Mongodb",
    response_description="ACK with the name of the file uploaded", response_model=FileResponse)
async def upload_file(file: UploadFile = File(description="CSV with the required audit structure")):
    if (not file):
        raise HTTPException(400, detail="File not found!")

    if not file.content_type in FILE_TYPES:
        raise HTTPException(400, detail="Invalid document type")

    arr = csvToJson(file)

    for item in arr:
        newItem = pickFields(item, DEFAUTL_FIELDS)
        newItem["createdDate"] = parseDate(item["createdDate"])
        newItem["modifiedDate"] = parseDate(item["modifiedDate"])

        await collection.insert_one(newItem)

    return {"message": file.filename + " uploaded!"}


@app.get("/get_items", description="Search the audit records by diferent criteria",
    response_description="List with the filters applied", response_model=List[AuditResponse])
async def find_audit_items(
    transactionId: Union[str, None] = Query(default=None, example="868add4b-42ae-4325-a583-efc13dd3e628"),
    workflowId: Union[str, None] = Query(default=None, example="6390e4e1c2c3b639b3e9b272"),
    startDate: Union[date, None] = Query(default=None, example="2008-09-15", description="Search the date range. This is the initial date"),
    endDate: Union[date, None] = Query(default=None, example="2008-09-15", description="Search the date range. This is the final date"),
    user: Union[str, None] = Query(default=None, example="user2"),
    client: Union[str, None] = Query(default=None, example="client1"),
    action: Union[str, None] = Query(default=None, example="action5"),
    sortedByDate: Union[bool, None] = Query(default=False, description="Get List sorted by Date (from recent to last)"),
):
    query = buildQuery(transactionId, workflowId, startDate, endDate, user, client, action)
    cursor = collection.find(query)

    DEFAULT_LIMIT = 10000

    if (sortedByDate):
        resSorted = await cursor.sort('modifiedDate', -1).to_list(DEFAULT_LIMIT)
        return parseResponse(resSorted, DEFAUTL_FIELDS)

    res = await cursor.to_list(DEFAULT_LIMIT)
    return parseResponse(res, DEFAUTL_FIELDS)
