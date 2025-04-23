# M1Macの場合は以下を指定
FROM python:3.12
# それ以外の場合は以下を指定
# ! 注意:slim版だとpylanceの自動importが効かない
# FROM python:3.11-slim

# パッケージのインストール
RUN apt-get update -qq \
   && apt-get install -y --no-install-recommends \
   tzdata sudo \
   && rm -rf /var/lib/apt/lists/*

# モジュールのインストール
WORKDIR /tmp/work
COPY requirements.txt ${PWD}
# RUN  pip install -upgrade pip
RUN  pip install -r requirements.txt

# 環境変数の定義
ENV TZ="Asia/Tokyo"

# 太田 和樹. Docker Desktop for Windows/Macでつくるクリーンな開発環境構築入門(Python版) (pp.498-499). Kindle 版.
# 一時変数の定義
ARG USERNAME=user1
ARG PASSWORD=user1
ARG GROUPNAME=user1
ARG UID=1000
ARG GID=1000

# 一般権限のユーザーを追加
RUN groupadd -g ${GID} ${GROUPNAME} \
 && useradd -u ${UID} -g ${GID} -G sudo -m -s /bin/bash ${USERNAME} \
 && echo ${USERNAME}:${PASSWORD} | chpasswd \
 && echo "%${USERNAME} ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# ユーザーの切替
USER ${USERNAME}
