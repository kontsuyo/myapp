#!/bin/bash

curl \
-X POST \
-H "Content-Type: application/json" \
-d '{"username": "fuga", "password": "fugafuga"}' http://127.0.0.1:8000/users/login/ \
| jq
