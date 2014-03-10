#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import stderr, argv
import elasticsearch
from pymongo import MongoClient
from csv import DictReader

if len(argv) > 1:
    try:
        with open(argv[1]) as f:
            twiter = list(DictReader(f))
    except:
        stderr.write("Could not load json data in %s\n" % argv[1])
        exit(1)
else:
    twiter = MongoClient().gazouilleur.tweets.find()

try:
    with open("stopwords.fr.txt") as stw:
        stopwords = u",".join(stw.read().decode('utf-8').split('\n'))
except:
    stderr.write("ERROR: Could not open stopwords.fr.txt file\n")
    exit(1)

es = elasticsearch.Elasticsearch()
try:
    esco = elasticsearch.client.IndicesClient(es)
    try:
        esco.delete(index="twitter", master_timeout=30, timeout=1800)
    except elasticsearch.exceptions.NotFoundError:
        pass
    esco.create(index="twitter",
      body={
        "settings": {"analysis" : {"analyzer": {"tweettext": {
          #"type": "french",
          "type": "standard",
          "stopwords": stopwords
        } } } },
        "mappings": {"tweets": {"properties": {
          "date": {"type": "date"},
          "message": {"type": "string", "store": "yes", "analyzer": "tweettext"},
          "screenname": {"type": "string", "store": "yes", "index": "not_analyzed"},
          "uniq_rt_hash": {"type": "string", "store": "yes", "index": "not_analyzed"}
        } } }
      }, master_timeout=30, timeout=60)
except Exception as e:
    stderr.write("ERROR: Could not recreate index in ElasticSearch:\n %s %s\n" % (type(e), e))
    exit(1)


for tweet in twiter:
  try:
    if '_id' in tweet:
        del(tweet['_id'])
    es.index(
        index="twitter",
        doc_type="tweets",
        body=tweet
    )
  except Exception as e:
    stderr.write("ERROR %s: %s\n -> %s\n" % (type(e), e, tweet))
