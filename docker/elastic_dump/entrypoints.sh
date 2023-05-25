#!/usr/bin/env bash

elasticdump --output=http://elastic:9200/genres --input=/dumps/genres_settings.json --type=settings --limit=1000
elasticdump --output=http://elastic:9200/persons --input=/dumps/persons_settings.json --type=settings --limit=1000
elasticdump --output=http://elastic:9200/movies --input=/dumps/movies_settings.json --type=settings --limit=1000

elasticdump --output=http://elastic:9200/genres --input=/dumps/genres_mapping.json --type=mapping --limit=1000
elasticdump --output=http://elastic:9200/persons --input=/dumps/persons_mapping.json --type=mapping --limit=1000
elasticdump --output=http://elastic:9200/movies --input=/dumps/movies_mapping.json --type=mapping --limit=1000

elasticdump --output=http://elastic:9200/genres --input=/dumps/genres.json --type=data --limit=1000
elasticdump --output=http://elastic:9200/persons --input=/dumps/persons.json --type=data --limit=1000
elasticdump --output=http://elastic:9200/movies --input=/dumps/movies.json --type=data --limit=1000