from pymongo import MongoClient
import util
import copy

def refresh_blocks(history):
    client = MongoClient('mongodb://localhost:3001/')
    db = client.meteor
    blocks = db['blocks']
    if blocks.find_one({})['hash'] != history[0]['hash']:
        blocks.delete_many({})

        for row in history:
            to_insert = copy.deepcopy(row)
            to_insert['amount'] = util.raw_to_nanostr(to_insert['amount'], to_insert['type'])
            blocks.insert_one(to_insert)
