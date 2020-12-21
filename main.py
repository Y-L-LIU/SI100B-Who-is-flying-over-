import web_server.server
from cli.cli import cli_start
import os
import sys
import logging
import webbrowser



def _help():
    print("Usage:")
    print()
    print("  {} --web | --cli".format(sys.argv[0]))
    print()
    print("If you choose to implement the CLI (easy level), run:")
    print()
    print("  {} --cli".format(sys.argv[0]))
    print()
    print("If you choose to implement the web server (advanced level), run:")
    print()
    print("  {} --web".format(sys.argv[0]))
    print()

if __name__ == "__main__":
    logger = logging.getLogger("si100b_proj:main")
    logger.setLevel("INFO")

    if len(sys.argv) != 2:
        logger.error("Except 1 argument, get {}.".format(len(sys.argv) - 1))
        _help()
        exit(-1)
    if not (sys.argv[1] == "--web" or sys.argv[1] == "--cli"):
        logger.error("Invalid argument.")
        _help()
        exit(-1)
    else:
        flag = sys.argv[1]

    ppid = os.getppid()
    try:
        if flag == '--web':
            web_server.server.start(logger)
        elif flag == '--cli':
            cli_start(logger)
    except KeyboardInterrupt:
        logger.warning("Control panel exits.")
        os.kill(ppid)

        