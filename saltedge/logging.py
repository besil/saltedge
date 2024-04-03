import logging

log = logging.getLogger("saltedge")

if not log.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        # name
        "[%(asctime)s][%(levelname)8s][%(module)30.30s]@[%(lineno)5s]$ %(message)s"
    )
    handler.setFormatter(formatter)
    log.addHandler(handler)

    log.setLevel(logging.DEBUG)
