import bottle
import sys
from pyroxy import app, config


if len(sys.argv) != 2:
    print >> sys.stderr, "No config file specified."
    print >> sys.stderr, "Usage: %s config_file" % sys.argv[0]
    sys.exit(1)

config.load_config(sys.argv[1])
bottle.debug(True)
bottle.run(app, host="localhost", port=5000, reloader=True)
