defmodule TaskManager.MixProject do
  use Mix.Project

  def project do
    [
      app: :task_manager,
      version: "0.1.0",
      elixir: "~> 1.13",
      start_permanent: Mix.env() == :prod,
      deps: deps()
    ]
  end

  defp deps do
    []
  end
end
