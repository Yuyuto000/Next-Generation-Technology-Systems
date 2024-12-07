defmodule TaskManager.Supervisor do
  use Supervisor

  def start_link(_) do
    Supervisor.start_link(__MODULE__, nil, name: __MODULE__)
  end

  def init(_) do
    children = [
      {Registry, keys: :unique, name: TaskManager.TaskRegistry}
    ]

    Supervisor.init(children, strategy: :one_for_one)
  end
end
