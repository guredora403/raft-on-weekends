# Raft on Weekends

Delight 2024の夏合宿用。
このレポジトリはRaftを作成するためのひな形を提供します。
具体的にはノード間が実装されています。
この上にRaftの機能（RequestVote, AppendEntries）を実装します。

## ファイル構成

- `run_node.py`: ノードを起動するためのスクリプトファイル
- `Dockerfile`: Dockerイメージをビルドするための設定ファイル。
- `docker-compose.yml`: 複数のDockerコンテナを定義し、ノード間のネットワークを設定するためのファイル。
- `generate_docker_compose.py`: 指定されたノード数に基づいて`docker-compose.yml`を動的に生成するPythonスクリプト。

## 必要な環境

- Docker
- Docker Compose
- Python 3.x (with pyyaml)


## セットアップ手順

1. **リポジトリをクローン**

   ```bash
   git clone https://github.com/mzhkz/raft-on-weekends.git
   cd raft-on-weekends
   ```

2. **必要なライブラリをインストール**

   ```bash
   pip install pyyaml
   ```


3. **docker-composeファイルの作成**

   ```bash
   python generate_docker_compose.py <ノードの数>
   ```

4. **docker-composeを用いてコンテナ（ノード）を作成**

   ```bash
   docker compose up -d --build
   ```

5. **開発ログを見る場合**

   ```bash
   docker logs node{1~ノードの数} -f
   ```
