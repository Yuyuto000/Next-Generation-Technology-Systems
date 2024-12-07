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


#### `lib/task_manager/task.ex` (タスクモジュール)

```elixir
defmodule TaskManager.Task do
  defstruct id: nil, name: nil, status: :pending

  def start_task(%TaskManager.Task{id: id} = task) do
    IO.puts("Starting task #{id}: #{task.name}")
    %{task | status: :in_progress}
  end

  def complete_task(task) do
    IO.puts("Completing task #{task.id}: #{task.name}")
    %{task | status: :completed}
  end
end
