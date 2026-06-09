# Watccher is for local dev. For depolyment I might go with google drive pooling with drive integration.

import os
import django

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "backend.settings"
)

django.setup()

import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


from myapi.services.process_audio import process_audio


class RecordingHandler(FileSystemEventHandler):

    def on_created(self, event):

        if event.is_directory:
            return

        if not event.src_path.endswith((".m4a", ".mp3", ".wav")):
            return

        print(f"New recording detected: {event.src_path}")

        # giving zoom to finish recording 
        time.sleep(30)

        try:
            print("Processing recording")

            process_audio(event.src_path)
            

            os.remove(event.src_path)

            print("Recording processed successfully")

        except Exception as e:
            print(f"Processing failed: {e}")


def start_watcher(folder_path):

    observer = Observer()

    observer.schedule(
        RecordingHandler(),
        path=folder_path,
        recursive=False
    )

    observer.start()

    print(f"Watching folder: {folder_path}")

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        observer.stop()

    observer.join()


if __name__ == "__main__":

    start_watcher(
        r"E:\IB PE Meeting Bot\recordings"
    )