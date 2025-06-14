#!/bin/bash

curl \
-X GET \
-H "Content-Type: application/json" http://127.0.0.1:8000/testuser/ \
| jq
