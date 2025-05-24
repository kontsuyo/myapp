#!/bin/bash

curl \
-X PATCH \
-H "Authorization: Token 6b6dd034009398f112dfd59e68613c6aec32464d" \
-H "Content-Type: application/json" \
-d '{"username": "updatehoge"}' http://127.0.0.1:8000/users/update_account/ \
| jq
