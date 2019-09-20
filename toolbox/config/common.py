CURRENT_MIN_VERSION = 'v3.0'
CURRENT_MAX_VERSION = 'v3.1'

ACTIVE_REMOTE_BRANCHES = ['master', 'staging', 'demo']
DEFAULT_COMMAND_TIMEOUT = 60 * 60

CONTROLLER_PROTOCOL = 'controller'
PROTOCOLS = {'udp', 'tcp', 'ssh', 'http', 'ws', CONTROLLER_PROTOCOL}
CRP_TYPES = {'docker', 'gce', 'static'}