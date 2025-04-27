# M1Macの場合は以下を指定
FROM python:3.12-slim
# それ以外の場合は以下を指定
# ! 注意:slim版だとpylanceの自動importが効かない
# FROM python:3.11-slim

# パッケージのインストール
RUN apt-get update -qq \
   && apt-get install -y --no-install-recommends \
   tzdata sudo \
   && rm -rf /var/lib/apt/lists/*

# 作業ディレクトリの作成
WORKDIR /tmp/work

# Pythonモジュールのインストール
COPY requirements.txt .
RUN  pip install -r requirements.txt

# タイムゾーンの設定
ENV TZ="Asia/Tokyo"

# ユーザー・グループ情報
ARG USERNAME=user1
ARG GROUPNAME=user1
ARG UID=1000
ARG GID=1000

# 一般ユーザー作成
RUN groupadd -g ${GID} ${GROUPNAME} \
 && useradd -u ${UID} -g ${GID} -G sudo -m -s /bin/bash ${USERNAME} \
 && echo "%${USERNAME} ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# 一般ユーザーに切替
USER ${USERNAME}
