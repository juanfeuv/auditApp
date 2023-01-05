def pickFields(di, fields):
    newDict = {}

    for i in fields:
        newDict[i] = di[i]

    return newDict