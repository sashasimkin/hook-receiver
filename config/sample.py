# Path to project root, this is cwd for all spawned commands
PATH = '../test/'
# List of refs that to be substituted to re.compile(REFS.%i%).match(request.data.refs)
REFS = ['refs/heads/.*', '.*']
# List of commands, that will be spawned
COMMANDS = [
    ''
]