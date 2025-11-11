from pymongo import MongoClient
import requests, os, datetime

now = datetime.datetime.utcnow()
one_hour_ago = now - datetime.timedelta(hours=1)

client = MongoClient(os.environ["MONGO_URI"])
col = client["yourDB"]["Target_P4_Opt"]

hourly = col.count_documents({
    "gpost_date": {"$gt": one_hour_ago, "$lte": now},
    "gpost": 5.0,
    "job_status": {"$ne": "3.0"}
})
total = col.count_documents({"gpost": 5.0})
queued = col.count_documents({"job_status": "pending"})

msg = f"📊 Jobs: {hourly} last hour | {total} total | {queued} queued"
requests.post(os.environ["DISCORD_WEBHOOK"], json={"content": msg})

client.close()
