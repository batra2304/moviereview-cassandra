import json
import multiprocessing as mp
import cassandra
from cassandra.query import BatchStatement

from cassandra.cluster import Cluster

cluster = Cluster(['127.0.0.1'])
session = cluster.connect()

# Create keyspace and table
session.execute(
    "CREATE KEYSPACE IF NOT EXISTS movie_keyspace WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 3 }")
session.execute("CREATE TABLE IF NOT EXISTS movie_keyspace.reviews (review_id text PRIMARY KEY,reviewer text,movie text,rating text,review_summary text,review_date text,spoiler_tag int,review_detail text,helpful List<text>)")


def insert_batch(batch):
    batch_stmt = BatchStatement()
    for item in batch:
        # idd = item.pop("review_id", None)
        # Insert data into Cassandra table
        #     session.execute("INSERT INTO movie_keyspace.reviews (review_id, data) VALUES (%s, %s)", (data['review_id'], data))
        query = '''
                INSERT INTO movie_keyspace.reviews (review_id,reviewer,movie,rating,review_summary,review_date,spoiler_tag,review_detail,helpful) VALUES (%s, %s, %s,%s, %s, %s,%s, %s, %s)
                '''
    #     batch_stmt.add(query, (item['review_id'],item['reviewer'],item['movie'],item['rating'],item['review_summary'],item['review_date'],item['spoiler_tag'],item['review_detail'],item['helpful']))
    # session.execute(batch_stmt)
        session.execute_async(query, (item['review_id'],item['reviewer'],item['movie'],item['rating'],item['review_summary'],item['review_date'],item['spoiler_tag'],item['review_detail'],item['helpful']))


with open('/home/rajat/Downloads/archive/part-01.json', 'r') as f:
    data = json.load(f)

num_processes = 4

batch_size = len(data) // num_processes
batches = [data[i:i + batch_size] for i in range(0, len(data), batch_size)]

# with mp.Pool(processes=num_processes) as p:
#     p.map(insert_batch, batches)
#     p.close()
#     p.join()
insert_batch(data)