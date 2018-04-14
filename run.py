# -*- coding: utf-8 -*-

import signal
from threading import Event

from moo import app, download_queue, convert_queue, upload_queue, delete_queue, done_queue
from moo.signal_handler import SignalHandler
from moo.worker import Worker, download_from_youtube, convert_to_mp3, upload_to_drive, delete_local_file

if __name__ == "__main__":
    workers_per_thread = 1
    stopper = Event()

    threads = []

    for _ in range(workers_per_thread):
        threads.append(Worker(download_from_youtube, download_queue, convert_queue, stopper))
        threads.append(Worker(convert_to_mp3, convert_queue, upload_queue, stopper))
        threads.append(Worker(upload_to_drive, upload_queue, delete_queue, stopper))
        threads.append(Worker(delete_local_file, delete_queue, done_queue, stopper))

    handler = SignalHandler(threads, stopper)
    signal.signal(signal.SIGINT, handler)

    for thread in threads:
        thread.start()

    app.run(host='0.0.0.0')
