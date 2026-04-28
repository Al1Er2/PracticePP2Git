import os
from configparser import ConfigParser

def load_config(filename='database.ini', section='postgresql'):
    # Get the directory where config.py is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, filename)

    parser = ConfigParser()
    if not os.path.exists(file_path):
        raise Exception(f'File {filename} not found at {file_path}')
        
    parser.read(file_path)

    # get section, default to postgresql
    config = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            config[param[0]] = param[1]
    else:
        raise Exception(f'Section {section} not found in the {filename} file')
    return config

if __name__ == '__main__':
    config = load_config()
    print("Database configuration loaded:", config)