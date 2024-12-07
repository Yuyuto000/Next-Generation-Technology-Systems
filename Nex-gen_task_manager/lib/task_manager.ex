defmodule TaskManager do
  alias TaskManager.{Task, Worker, Supervisor}

  # Supervisorを開始
  def start() do
    {:ok, _pid} = Supervisor.start_link(nil, [])
  end

  # 新しいタスクを追加
  def add_task(name) do
    task = %Task{id: :erlang.unique_integer([:positive]), name: name}
    worker_pid = Worker.start_link(task)
    Worker.start_task(worker_pid)
  end

  # タスクの状態をリストアップ
  def list_tasks() do
    TaskManager.TaskRegistry
    |> Registry.select([{{:_, :_, :_}, [], [self()]})
    |> Enum.each(fn pid -> IO.inspect(pid) end)
  end
end
