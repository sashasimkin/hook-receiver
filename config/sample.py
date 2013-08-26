# Path to project root, this is cwd for all spawning commands
PATH = '../test/'
# List of refs that to be substituted to re.compile(REFS.%i%).match(request.data.refs)
REFS = ['refs/heads/.*', '.*']
# List of commands, that will be spawned
COMMANDS = [
    ''
]


# Hooks
def ref_not_fit(test_ref, payload):
    """
        Function called if ref doesn't fit

    :param test_ref: ref string which failed test from `REFS`
    :param payload: Request payload
    :return:
    """
    pass


def on_command(command, payload):
    """
        Function called on any command

    :param command: Command which will be spawned
    :param payload: Request payload
    :return:
    """
    pass


def on_error(exception, payload):
    """
        Function called on any error

    :param exception: Raised exception
    :param payload: Request payload
    :return:
    """
    pass