from pyroxy import app as application, config

config_path = os.environ['PYROXY_CONFIG']
config.load_config(config_path)
