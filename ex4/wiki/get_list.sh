#!/bin/bash

curl $1 | grep '<li><a href=' | sed 's/<li><a href="//' | sed -r 's/" .+//' | sed 's/<ul>//' | grep wiki