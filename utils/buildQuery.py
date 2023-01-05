from .parseToDate import parseToDate

def buildQuery(transactionId, workflowId, startDate, endDate, user, client, action):
    query = {}

    if (transactionId):
        query["transactionId"] = transactionId

    if (workflowId):
        query["workflowId"] = workflowId

    if (startDate or endDate):
        queryDate = {}
        if startDate:
            queryDate["$gte"] = parseToDate(startDate)

        if endDate:
            queryDate["$lte"] = parseToDate(endDate)

        query["modifiedDate"] = queryDate

    if (user):
        query["userId"] = user

    if (client):
        query["clientId"] = client

    if (action):
        query["action"] = action

    return query