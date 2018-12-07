
# 

## datafield
``
PUT flows/packet/_doc
{
  "properties": {
    "protocolName.keyword": { 
      "type":     "text",
      "fielddata": true
    }
  }
}
``


## delete all data of an index
````
curl -X DELETE "localhost:9200/my_index"
````

