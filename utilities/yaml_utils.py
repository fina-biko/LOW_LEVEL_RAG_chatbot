import yaml

file_path='config/config.yaml'
from typing import Dict

def read_yaml_log_path(file_path: str = file_path) -> Dict[str, str]:
    
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
    return config


if __name__ == "__main__":
    config = read_yaml_log_path('config/config.yaml')
    print(config)