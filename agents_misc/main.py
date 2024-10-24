from agent_generator import generate_agent
from master_agent import MasterAgent


def main():
    # Generate agents
    generate_agent('agents/agent_configs/agent1.yaml', 'agent1_graph.jinja', 'base_agent.jinja',
                   'agents/generated/agent1.py')
    generate_agent('agents/agent_configs/agent2.yaml', 'agent2_graph.jinja', 'base_agent.jinja',
                   'agents/generated/agent2.py')

    # Create and use MasterAgent
    master = MasterAgent('command_map.yaml')

    while True:
        command = input("Enter a command (or 'quit' to exit): ")
        if command.lower() == 'quit':
            break
        try:
            result = master.execute_command(command)
            print(f"Result: {result}")
        except ValueError as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()