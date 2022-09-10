import yaml

class Channel():
    def __init__(self, config):
        with open(config, 'r') as f:
            keys = yaml.safe_load(f)

        self.name = keys['tg_keys']['name']
        self.geos = keys['geo']
        self.companies = keys['companies']
        self.refs = keys['refs']
        self.chat_id = keys['tg_keys']['chat_id']
        self.token = keys['tg_keys']['token']
        return
