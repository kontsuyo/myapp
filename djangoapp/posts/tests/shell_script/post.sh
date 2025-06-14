#!/bin/bash

curl \
-X POST \
-H "Authorization: Token 83e252951a9369e88f1bce1bb2a1b8af7586b4cc" \
-H "Content-Type: application/json" \
-d '{"content": "私はこのポストを削除する予定だ。"}' http://127.0.0.1:8000/ \
| jq
