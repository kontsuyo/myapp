#!/bin/bash

curl \
-X PATCH \
-H "Content-Type: application/json" \
-d '{"username": "updatehoge"}' http://127.0.0.1:8000/users/update_account/ \
| jq
