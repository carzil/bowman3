import logging

formatter = logging.Formatter("(%(levelname)s)[%(name)s]: %(message)s")

fh = logging.FileHandler("worker.log")
sh = logging.StreamHandler()
fh.setFormatter(formatter)
sh.setFormatter(formatter)

worker_log = logging.getLogger("server")
worker_log.setLevel(logging.DEBUG)
worker_log.addHandler(fh)
worker_log.addHandler(sh)
