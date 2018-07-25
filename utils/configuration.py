import yaml
import os

CONFIG_DIRECTORY = 'configuration'


def get_config(path):
    f = open(path)
    return yaml.load(f)


def load():
    configuration = {}
    configs_to_load = ['database', 'app_config']
    for config in configs_to_load:
        path = os.path.join(CONFIG_DIRECTORY, config+'.yaml')
        configuration[config] = get_config(path)
    return configuration
