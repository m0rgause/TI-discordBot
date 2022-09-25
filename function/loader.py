from time import time


import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


def on_modified(event):
    if event.src_path == "../lib/message.py":
        print("File has been updated")


def nocache():
    event_handler = FileSystemEventHandler()
    event_handler.on_modified = on_modified
    observer = Observer()
    observer.schedule(event_handler, ".", recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(2)
    finally:
        observer.stop()
        observer.join()
