import yaml
import importlib


class MasterAgent:
    def __init__(self, command_map_file):
        with open(command_map_file, 'r') as file:
            self.command_map = yaml.safe_load(file)

    def execute_command(self, command):
        for cmd in self.command_map['commands']:
            if cmd['command'] == command:
                agent_module = importlib.import_module(f"agents.generated.{cmd['agent'].lower()}")
                agent_class = getattr(agent_module, cmd['agent'])
                agent = agent_class()
                return agent.run(command)
        raise ValueError(f"Unknown command: {command}")