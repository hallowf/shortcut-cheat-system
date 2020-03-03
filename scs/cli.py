import sys
import keyboard
import time
import argparse
import logging
from backend.scs_classes import Backend

# Sets up logger and returns it
def set_up_logger(log_level):
    n_level = getattr(logging, log_level.upper(), 10)
    # Console logger
    log_format = "%(name)s - %(levelname)s: %(message)s"
    logging.basicConfig(format=log_format, level=n_level)
    logger = logging.getLogger("SCS-CLI")
    msg = "%s: %s" % ("Console logger is set with log level", log_level)
    logger.info(msg)
    return logger

# Verifies and fixes log level if invalid
def verify_log_level(log_level):
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
    return log_level

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
    logger = None
    try:
        args = parse_and_return_args()
        log_level = verify_log_level(args.log_level)
        logger = set_up_logger(log_level)
        b = Backend(args.process, args.cheats_file,
                    args.end_combination, True, log_level=log_level)
        b.hook_keys()
        logger.info("SCS running. Press %s or ctrl+c to exit" % args.end_combination)
        b.run()
        logger.info("Exiting")
        sys.exit(0)
    except Exception as e:
        raise e
        # if logger != None:
        #     logger.error(str(e))
        # else:
        #     sys.stdout.write("Error: %s" % str(e))
