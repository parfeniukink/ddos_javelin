###########################################
# ARGPARSER
###########################################
ARGPARSER_WELCOME_MESSAGE = "DDoS Javelin arguments parser"
IP_REGEX = r"^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$"
ADDRESS_REGEX = r"^[\w.]+(\.[\w\.]+)+[\w\._~:/?#[\]@!\$&'\(\)\*\+,;=.]+$"


###########################################
# FILENAMES
###########################################
REFERERS_FILENAME = "static/referers.txt"
USER_AGENTS_FILENAME = "static/user_agents.txt"


###########################################
# PACKETS
###########################################
CRLF = r"\n\r"


###########################################
# OTHER
###########################################
MIN_PORT_NUMBER = 5
MAX_PORT_NUMBER = 65535
