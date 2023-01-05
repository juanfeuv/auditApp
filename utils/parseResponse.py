from .pickFields import pickFields

DATE_FORMAT = "%m/%d/%Y"

def trasform(fields):
    def every(x):
        newI = pickFields(x, fields)
        newI["createdDate"] = x["createdDate"].strftime(DATE_FORMAT)
        newI["modifiedDate"] = x["modifiedDate"].strftime(DATE_FORMAT)

        return newI

    return every


def parseResponse(li, fields):
    res = map(trasform(fields), li)

    return list(res)
