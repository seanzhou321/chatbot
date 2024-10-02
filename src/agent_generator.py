import yaml
from jinja2 import Environment, FileSystemLoader
import os

def generate_agent(config_file, graph_file, template_file, output_file):
    # Load configuration
    with open(config_file, 'r') as file:
        config = yaml.safe_load(file)

    # Set up Jinja2 environment
    env = Environment(loader=FileSystemLoader('agents/agent_templates'))

    # Load and render agent template
    agent_template = env.get_template(template_file)
    agent_code = agent_template.render(config)

    # Load and render graph template
    graph_template = env.get_template(graph_file)
    graph_code = graph_template.render(agent_name=config['name'])

    # Combine agent and graph code
    full_code = f"{agent_code}\n\n{graph_code}"

    # Write to output file
    with open(output_file, 'w') as file:
        file.write(full_code)