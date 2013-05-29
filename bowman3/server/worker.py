from .loggers import worker_log
import socket
import threading
import time
import select
import os
import atexit
import struct
from signal import signal, SIGTERM
from .packages.core import Package
from .player import Player

QUEUE_CHECK_TIMEOUT = 0.5
NOTICE_TIMEOUT = 10

class Worker():
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self._is_running = threading.Event()

    def _init_worker(self):
        worker_log.info("spawned worker, pid={}".format(os.getpid()))

        self._track = []
        self._players = {}

        self._is_running.set()

        self._socket = None

        self._packages_map = {}
        self._package_queue = []

        self._register_packages()

        atexit.register(self._stop)
        signal(SIGTERM, self._sigterm_handler)
        worker_log.info("worker initialization passed successfully")

    def _register_packages(self):
        self._packages_map = {}
        cnt = 0
        for klass in Package.__subclasses__():
            self._packages_map[klass.PACKAGE_ID] = klass
            cnt += 1
        worker_log.info("register %d packages", cnt)

    def _sigterm_handler(self, signum, frame):
        self._stop()
        os._exit(0)

    def _create_socket(self):
        '''
        Creates socket instance and saves as `self._socket`.
        '''
        self._socket = socket.socket()
        # Special hack for address in use problem
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        worker_log.info("socket created")

    def _bind_socket(self):
        '''
        Binds socket `self._socket` to `self.host` and `self.port`.
        '''
        self._socket.bind((self.host, self.port))
        self._socket.listen(5)
        worker_log.info("socket binded to %s:%d", self.host or "*", self.port)

    def _start_in_thread(self, func, args=(), kwargs={}):
        '''
        Start function `func` in separate thread.
        `args` and `kwargs` is arguments and keyword arguments.
        Returns `threading.Thread` object.
        '''
        thread = threading.Thread(target=func, args=args, kwargs=kwargs)
        thread.start()
        return thread

    def _serve_queue(self):
        '''
        Packages queue server. Queue is a list object `self._package_queue`.
        '''
        # CODE FOR DEBUG. DELETE FROM PRODUCTION.
        # last_noticed_time = time.time()

        while self._is_running.is_set():
            # CODE FOR DEBUG. DELETE FROM PRODUCTION.
            # t = time.time()
            # if t - last_noticed_time >= NOTICE_TIMEOUT:
            #     last_noticed_time = t
            #     worker_log.debug("queue length = %d", len(self._package_queue))
            try:
                if self._package_queue:
                    package, player = self._package_queue.pop(0)
                    try:
                        package.handle(player)
                    except:
                        worker_log.exception("exception occured in package handler")
                else:
                    time.sleep(QUEUE_CHECK_TIMEOUT)
            except:
                worker_log.exception("exception occured, ignoring")

    def _handle_new_client(self, addr, sock):
        p = Player(sock, addr)
        self._track.append(sock)
        self._players[sock] = p
        worker_log.info("handled new client at %s:%d", *addr)

    def _handle_client_disconnect(self, sock, player):
        self._players.pop(sock)
        self._track.remove(sock)
        sock.close()
        worker_log.info("'%s:%d' disconnected", player.host, player.port)
        del player

    def _handle_new_request(self, sock):
        p = self._players.get(sock)
        p_magic_short = sock.recv(2)
        if not p_magic_short:
            return self._handle_client_disconnect(sock, p)
        p_magic = struct.unpack(">H", p_magic_short)[0]
        p_type = self._packages_map.get(p_magic)
        if p_type is None:
            worker_log.info("client sent invalid package, ignoring it")
        else:
            try:
                package = p_type.load(sock)
            except:
                worker_log.exception("cannot receive package from client's socket:")
            else:
                self._package_queue.append((package, p))
                worker_log.info("added a package from player at %s:%d to queue", p.host, p.port)

    def _stop(self):
        worker_log.info("initiated server stopping")
        self._is_running.clear()
        worker_log.info("waiting for terminating threads")
        while threading.active_count() > 1:
            pass
        worker_log.info("threads terminated")
        if self._socket:
            self._socket.close()
        worker_log.info("server socket closed")

    def _start(self):
        try:
            self._create_socket()
            self._bind_socket()
            self._track.append(self._socket)
            self._start_in_thread(self._serve_queue)

            while self._is_running.is_set():
                r, w, x = select.select(self._track, [], [])

                for sock in r:
                    if sock is self._socket:
                        conn, addr = self._socket.accept()
                        self._handle_new_client(addr, conn)
                    else:
                        self._handle_new_request(sock)

        except KeyboardInterrupt:
            self.stop()
        except:
            worker_log.exception("unhandled exception occured, aborting")

    def run(self):
        self._init_worker()
        self._start()
