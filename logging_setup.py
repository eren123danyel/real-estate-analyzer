import sys
import logging
from logging.handlers import RotatingFileHandler
from colorlog import ColoredFormatter

def setup_logging(
    level=logging.INFO,
    logfile="real-estate-analyzer.log",
    max_bytes=5_000_000,
    backups=3,
):
    root = logging.getLogger()
    root.setLevel(level)
    for h in list(root.handlers):
        root.removeHandler(h)

    # same look, with a tab before the message
    fmt_plain = "%(levelname)s:%(name)s:\t%(message)s"
    fmt_color = "%(log_color)s%(levelname)s%(reset)s:\t  %(message)s"

    # console (colored)
    sh = logging.StreamHandler(sys.stdout)
    sh.setLevel(level)
    sh.setFormatter(ColoredFormatter(
        fmt_color,
        log_colors={
            "DEBUG":    "cyan",
            "INFO":     "green",
            "WARNING":  "yellow",
            "ERROR":    "red",
            "CRITICAL": "bold_red",
        },
        secondary_log_colors={},
        style="%",                # use % formatting
    ))
    root.addHandler(sh)

    # file (plain, no color)
    fh = RotatingFileHandler(logfile, maxBytes=max_bytes, backupCount=backups, encoding="utf-8")
    fh.setLevel(level)
    fh.setFormatter(logging.Formatter(fmt_plain))
    root.addHandler(fh)