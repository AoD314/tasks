# Run user-selected command on many servers (user - provided as param) with ssh in parallel,
# collect output from all nodes.The script should print collected output from all nodes on stdout, w/o using temp files.
import subprocess
import threading
from optparse import OptionParser

outputs = {}

servers = ["127.0.0.1", "localhost"]


def run_remote_command(server, user, command):
    ssh_command = "ssh {}@{} {}".format(user, server, command)
    outputs[server] = subprocess.getoutput(ssh_command)


def main(command, user):
    threads = []
    for server in servers:
        thread = threading.Thread(target=run_remote_command, name=server, args=(server, user, command,))
        thread.start()

        threads.append(thread)

    for thread in threads:
        print('command: {}'.format(command))
        thread.join()
        output = outputs[thread.name]
        print('    {}'.format(output))
        print('-' * 80)


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-c", type=str, help="command to run on all servers")
    parser.add_option("-u", type=str, help="username")
    (options, _) = parser.parse_args()
    main(command=options.c, user=options.u)
