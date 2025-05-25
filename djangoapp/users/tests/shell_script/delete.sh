#!/bin/bash

curl \
-X DELETE \
-H "Content-Type: application/json" \
-H "Authorization: Token 940d6687a6f450e1803cc087f3e9cfaa56bf5357" \
http://127.0.0.1:8000/users/delete_account/
