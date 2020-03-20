import pymongo
import logging


def connect_to_mongodb(mongodb_instance: str, mongodb: str, mongodb_collection: str,
                       logger: logging.Logger)->pymongo.collection.Collection:
    """
    Connects to MongoDB and returns collection for further processing
    """
    stage_name = "MONGODB"
    client = pymongo.MongoClient(mongodb_instance)
    db = client[mongodb]
    collection = db[mongodb_collection]
    logger.info(f"{stage_name} - Connected to db '{mongodb}', collection '{mongodb_collection}'.")
    return collection


def record_json_to_mongodb(json_data: list, collection: pymongo.collection.Collection, logger: logging.Logger)->bool:
    """
    Records JSON data to MongoDB
    """
    stage_name = "MONGODB"
    result = collection.insert_many(json_data)
    if result.acknowledged:
        logger.info(f"{stage_name} - Recorded {len(json_data)} new results. Overall documents count - {collection.count_documents({})}")
        logger.debug(f"{stage_name} - Newly recorded IDS: {', '.join([str(id) for id in result.inserted_ids])}")
        return True
    else:
        logger.error(f"{stage_name} - JSON was not recorded to DB")
        return False


def find_flights_with_low_prices(threshold: int, search_date: str, collection: pymongo.collection.Collection,
                                 logger: logging.Logger)->None:
    """
    Finds flights with price lower than a threshold and returns all info for such flights
    (along with link to order tickets).
    """
    stage_name = "GET_MIN_PRICE"

    # calculate price for each itinerary (can have several Legs)
    price_per_flight_pipeline = [
        {"$match": {"Query.OutboundDate": search_date}},
        {"$unwind": "$Itineraries"},
        {"$project":
             {"Itineraries.OutboundLegId":
                  {"$arrayToObject":
                       [[{"k": "$Itineraries.OutboundLegId",
                          "v": {"$reduce":
                                    {"input": "$Itineraries.PricingOptions",
                                     "initialValue": 0,
                                     "in": {"$add":
                                                ["$$value",
                                                 "$$this.Price"]}}}
                          }]]}}}
    ]
    price_per_flight_results = collection.aggregate(price_per_flight_pipeline)

    # find flights with prices < threshold
    flights_with_low_prices = []
    for price_per_flight in price_per_flight_results:
        for k, v in price_per_flight['Itineraries']['OutboundLegId'].items():
            if v < threshold:
                flights_with_low_prices.append(k)

    logger.info(f"Found {len(flights_with_low_prices)} flights with prices lower than {threshold}")

    # return all flight data for resulted flights
    flights_data_pipeline = []  # TODO - request flights data from MongoDB

