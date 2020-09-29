from elasticsearch import helpers,Elasticsearch
import csv
import json
import pandas as pd
import numpy as np
import configparser

# config = configparser.ConfigParser()
# config.read('/Users/ins25k/Desktop/pycharm/djangoProject/WebCrawlerApp/logstash-csv.conf')

es=Elasticsearch()

INDEX="navernews"
TYPE= "record"

def rec_to_actions(df):
    import json
    for record in df.to_dict(orient="records"):
        yield ('{ "index" : { "_index" : "%s", "_type" : "%s" }}'% (INDEX, TYPE))
        yield (json.dumps(record, default=int))

from elasticsearch import Elasticsearch
if not es.indices.exists(INDEX):
    raise RuntimeError('index does not exists, use `curl -X PUT "localhost:9200/%s"` and try again'%INDEX)

# r = es.bulk(rec_to_actions(df)) # return a dict

# print(not r["errors"])





#dataframe->elasticsearch
# def doc_generator(dataframe):
#     df_iter=dataframe.iterrows()
#
#     for index,document in df_iter:
#         yield {
#             "_ index":"navernews",
#             "_type":"_doc",
#             "_id":f"{document['id']}",
#             "_source":filter(document),
#         }
#         raise StopIteration
#
# use_these_keys=['id','Title','ReplyIndex','CrawlingTime','Content','Like','Hate']
#
# def filterKeys(document):
#     return {key:document[key] for key in use_these_keys}
#
