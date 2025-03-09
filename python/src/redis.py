import redis
import datetime
import json

r = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
WRITE = True
PIPE = r.pipeline()

def delAll():
    r.flushdb()

def addPipeline(key, value):
    PIPE.set(key, value)

def executePipe():
    PIPE.execute()
    PIPE.reset()

def addItem(place, item_id, item):
    nitem = item.copy() 

    # Formatage des dates
    if "Datetime" in nitem:
        nitem["Datetime"] = nitem["Datetime"].strftime("%Y-%m-%d %H:%M:%S")
    if "Start" in nitem and nitem["Start"] is not None:
        nitem["Start"] = nitem["Start"].strftime("%Y-%m-%d %H:%M:%S")
    if "End" in nitem and nitem["End"] is not None:
        nitem["End"] = nitem["End"].strftime("%Y-%m-%d %H:%M:%S")
    if "datetime" in nitem:
        nitem["datetime"] = nitem["datetime"].strftime("%Y-%m-%d %H:%M:%S")
    if "Reference" in nitem:
        nitem["Reference"] = nitem["Reference"].strftime("%Y-%m-%d %H:%M:%S")

    # Supprimer des clés inutiles
    if "High datetime" in nitem:
        del nitem["High datetime"]
    if "Low datetime" in nitem:
        del nitem["Low datetime"]

    for key, value in nitem.items():
        if value is None:
            nitem[key] = ""

    item_key = f"{place}:{item_id}"

    addPipeline(item_key, json.dumps(nitem))

    return

def findCollection():
    name = "Backtest-"

    collections = r.keys(f"{name}*")
    collections = set([c.split(":")[0] for c in collections])
    collection = f"{name}{len(collections)}"

    return collection

def create_collection(collection_name):
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    params = {
        "Author": "Enzo Blain from Python",
        "Creation datetime": now_utc.isoformat(),
    }

    r.hset(f"{collection_name}:Informations", mapping=params)

def addCandle(collection_name, timerange, candle):
    place = f"{collection_name}:Data:{timerange}:Candles"
    id = str(int(candle["datetime"].timestamp()))
    addItem(place, id, candle)

def addSession(collection_name, session):
    place = f"{collection_name}:Data:Sessions"
    id = str(int(session["Start"].timestamp()))
    addItem(place, id, session)

def addFairValueGap(collection_name, timerange, fvg):
    place = f"{collection_name}:Data:{timerange}:FairValueGaps"
    id = str(int(fvg["Datetime"].timestamp()))
    addItem(place, id, fvg)

def addTrend(collection_name, timerange, trend):
    place = f"{collection_name}:Data:{timerange}:Trends"
    id = str(int(trend["Start"].timestamp()))
    addItem(place, id, trend)

def addBreakOfStructure(collection_name, timerange, bos):
    place = f"{collection_name}:Data:{timerange}:BreaksOfStructure"
    id = str(int(bos["Datetime"].timestamp()))
    addItem(place, id, bos)

def addChangeOfCharacter(collection_name, timerange, coc):
    place = f"{collection_name}:Data:{timerange}:ChangesOfCharacter"
    id = str(int(coc["Datetime"].timestamp()))
    addItem(place, id, coc)

def addOrderBlock(collection_name, timerange, ob):
    place = f"{collection_name}:Data:{timerange}:OrderBlocks"
    id = str(int(ob["Datetime"].timestamp()))
    addItem(place, id, ob)

def addRelativeHighsLows(collection_name, timerange, relative):    
    place = f"{collection_name}:Data:{timerange}:RelativeHighsLows"
    id = str(int(relative["Datetime"].timestamp()))
    addItem(place, id, relative)