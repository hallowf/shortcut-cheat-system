import sys
import keyboard
import time
import argparse
import logging
from backend.scs_classes import Backend

def install_logger(log_level):
    log_levels = [
        "INFO",
        "WARNING",
        "CRITICAL",
        "ERROR",
        "DEBUG"
    ]
    if log_level not in log_levels:
        sys.stdout.write("%s: %s\n" % ("Invalid log level", log_level))
        log_level = "INFO"
    n_level = getattr(logging, log_level.upper(), 10)
    # Console logger
    log_format = "%(name)s - %(levelname)s: %(message)s"
    logging.basicConfig(format=log_format, level=n_level)
    logger = logging.getLogger("SCS-CLI")
    msg = "%s: %s" % ("Console logger is set with log level", log_level)
    logger.info(msg)
    return logger


def verify_args(args):
    false_values = ["0", "FALSE"]
    if not args.cheats_file.endswith(".json"):
        raise ValueError("Invalid cheats file: %s" % args.cheats_file)
    args.verify_existence = False if args.verify_existence.upper() in false_values else True
    

def parse_and_return_args():
    parser = argparse.ArgumentParser(description='SCS - Shortcut Cheat System')
    parser.add_argument("process",
                        type=str,
                        help="Process name to write memory adresses")
    parser.add_argument("cheats_file",
                        type=str,
                        help="Path of the cheats file")
    parser.add_argument("end_combination",
                        type=str,
                        help="Key combination to terminate program")
    parser.add_argument("--verify-existence",
                        "--ve",
                        type=str,
                        default="True",
                        help="Verifies existence of process and cheats file")
    parser.add_argument("--log-level",
                        type=str,
                        default="info",
                        help="Log level for console logger")
    args = parser.parse_args()
    try:
        verify_args(args)
        return args
    except Exception:
        raise

if __name__ == '__main__':
    try:
        args = parse_and_return_args()
        install_logger(args.log_level)
        b = Backend(args.process, args.cheats_file,  args.end_combination, True)
        b.hook_keys()
        print("Running...\nPress ctrl+p+e or esc to exit")
        b.run()
        print("exiting")
        sys.exit(0)
    except Exception as e:
        raise e
