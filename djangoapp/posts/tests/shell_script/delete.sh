#!/bin/bash

curl \
-X DELETE \
-H "Authorization: Token 83e252951a9369e88f1bce1bb2a1b8af7586b4cc" \
-H "Content-Type: application/json" http://127.0.0.1:8000/testuser/delete/3 \
| jq
