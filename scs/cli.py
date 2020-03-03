import sys
import keyboard
import time
import argparse
import logging
from backend.scs_classes import Backend

def install_logger(l_level):
    l_levels = [
        "INFO",
        "WARNING",
        "CRITICAL",
        "ERROR",
        "DEBUG"
    ]
    n_level = None
    if l_level not in l_levels:
        sys.stdout.write("%s: %s\n" % (_("Invalid log level"), l_level))
        l_level = "INFO"
    n_level = getattr(logging, l_level.upper(), 10)
    # Console logger
    log_format = "%(name)s - %(levelname)s: %(message)s"
    logging.basicConfig(format=log_format, level=n_level)
    logger = logging.getLogger("STPDF-CLI")
    msg = "%s: %s" % (_("Console logger is set with log level"), l_level)
    logger.info(msg)
    return logger


def verify_args(args):
    print("verified")

def parse_and_return_args():
    parser = argparse.ArgumentParser(description=_('STPDF - easily convert scans to pdf'))
    parser.add_argument("source",
                        nargs="?",
                        type=str,
                        default=os.getcwd(),
                        help=_('Scan images location'))
    args = parser.parse_args()
    try:
        verify_args(args)
        return args
    except Exception:
        raise

if __name__ == '__main__':
    do_exit = False
    try:
        b = Backend("pcsx2", "godfather.json",  "esc", True)
        b.hook_keys()
        print("Running...\nPress ctrl+p+e or esc to exit")
        b.run()
        print("exiting")
        sys.exit(0)
    except Exception as e:
        raise e
