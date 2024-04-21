import mongo_db
import embedder 

def vector_search(user_query, collection):

    query_embedding = embedder.get_embedding(user_query)

    if query_embedding is None:
        return "Invalid query or embedding generation failed"

    pipeline = [
        {
            "$vectorSearch": {
                "index": "news_idx",
                "queryVector": query_embedding,
                "path": "News_embedding",
                "numCandidates": 25,
                "limit": 1,  # Return top 4 matches
            }
        },
        {
            "$project": {
                "_id": 0,
                "Name": 1,
                "Price": 1,
                "Change": 1,
                "Volume": 1,
                "Market Cap": 1,
                "News": 1,
                "score": {"$meta": "vectorSearchScore"},
            }
        },
    ]

    results = mongo_db.get_collection().aggregate(pipeline)
    return list(results)

def get_search_result(query, collection):

    get_knowledge = vector_search(query, mongo_db.get_collection())

    search_result = ""
    for result in get_knowledge:
        search_result += f"- Name: {result.get('Name', 'N/A')}, Price: {result.get('Price', 'N/A')}, Change: {result.get('Change', 'N/A')}, Volume: {result.get('Volume', 'N/A')}, Market Cap: {result.get('Market Cap', 'N/A')}, News: {result.get('News', 'N/A')}\n\n"

    return search_result