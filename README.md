# Gazouillanalyzer

Tryouts to visualize and analyze tweets stored by [Gazouilleur](http://github.com/RouxRC/gazouilleur) thanks to ElasticSearch and Kibana.


## Install

- Install [ElasticSearch](http://www.elasticsearch.org/overview/elasticsearch/):
```bash
wget https://download.elasticsearch.org/elasticsearch/elasticsearch/elasticsearch-1.0.1.deb
dpkg -i elasticsearch-1.0.1.deb
sudo service elasticsearch start
curl -X GET http://localhost:9200/ # This should display ElasticSearch's functionning status
```

- The [head plugin](https://github.com/mobz/elasticsearch-head) can also be useful to monitor the different indexes created in ElasticSearch:
```bash
sudo /usr/share/elasticsearch/bin/plugin -install mobz/elasticsearch-head
```
Access it here: [http://localhost:9200/_plugin/head/](http://localhost:9200/_plugin/head/)

- Install the python drivers to mongodb and ElasticSearch:
```bash
pip install -r requirements
```

- Install [Kibana](http://www.elasticsearch.org/overview/kibana/):
```bash
wget https://download.elasticsearch.org/kibana/kibana/kibana-3.0.0milestone5.tar.gz
tar xzvf kibana-3.0.0milestone5.tar.gz
sudo ln -s $(pwd)/kibana-3.0.0milestone5 /var/www/kibana
```
Access it here: [http://localhost/kibana](http://localhost/kibana)


## Run the indexer

- Without any argument, the script will try to connect to the current gazouilleur MongoDB:
```bash
./index.py
```

- Otherwise, to index an export of selected tweets:
```bash
./index.py tweets-transparence.csv
```
Assuming you exported data from gazouilleur earlier somehow like this:
```bash
mongoexport --db gazouilleur2 -u gazouilleur2 -p XXXXXXXX --collection tweets -v --csv -f id,link,screenname,message,date --query '{$query: {"channel": "#rc-veille", message: /transparen/i}}' -o tweets-transparence.csv
```


## Display stats

- Access Kibana locally: [http://localhost/kibana/](http://localhost/kibana/)
- Load the dashboard `kibana.conf` from the bar on the top right
- Explore...

