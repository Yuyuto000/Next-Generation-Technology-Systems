# TaskManager

分散型タスク管理システムです。このシステムはElixirのアクターモデルを使用して、タスクの並行処理と分配を行います。

## 使用方法

1. プロジェクトをクローン
2. `mix run` コマンドを実行して、タスクの管理を開始します。
3. タスクを追加するには、`TaskManager.add_task/1` を使用します。

## 実行例

```elixir
TaskManager.add_task("Task 1")
TaskManager.add_task("Task 2")
TaskManager.list_tasks()
