defmodule TaskManager.Worker do
  use GenServer

  def start_link(task) do
    GenServer.start_link(__MODULE__, task, name: via_tuple(task.id))
  end

  def init(task) do
    {:ok, task}
  end

  def handle_cast(:start_task, task) do
    updated_task = TaskManager.Task.start_task(task)
    {:noreply, updated_task}
  end

  def handle_cast(:complete_task, task) do
    updated_task = TaskManager.Task.complete_task(task)
    {:noreply, updated_task}
  end

  def via_tuple(id), do: {:via, Registry, {TaskManager.TaskRegistry, id}}

  def start_task(worker) do
    GenServer.cast(worker, :start_task)
  end

  def complete_task(worker) do
    GenServer.cast(worker, :complete_task)
  end
end
