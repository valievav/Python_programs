import pymongo
import logging


def connect_to_mongodb(mongodb_instance: str, mongodb: str, mongodb_collection: str,
                       logger: logging.Logger)->pymongo.collection.Collection:
    """
    Connects to MongoDB and returns collection for further processing
    """
    client = pymongo.MongoClient(mongodb_instance)
    db = client[mongodb]
    collection = db[mongodb_collection]
    logger.info(f"Connected to db '{mongodb}', collection '{mongodb_collection}'.")
    return collection


def record_json_to_mongodb(json_data: list, collection: pymongo.collection.Collection, logger: logging.Logger)->bool:
    """
    Records JSON data to MongoDB
    """
    result = collection.insert_many(json_data)
    if result.acknowledged:
        logger.info(f"Recorded {len(json_data)} new results. Overall documents count - {collection.count_documents({})}")
        logger.debug(f"Newly recorded IDS: {', '.join([str(id) for id in result.inserted_ids])}")
        return True
    else:
        logger.error(f"JSON was not recorded to DB")
        return False

