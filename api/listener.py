from time import sleep
from queue import Queue

from threading import Thread

from migration.migration import Migration, MigrationState
from persistence.migration import MigrationPickler


class Listener:
    def __init__(self):
        self.migration_pickler = MigrationPickler()

    def run(self, q: Queue):
        while True:

            while not q.empty():
                migration = q.get()
                self.migration_pickler.create(migration)
                Thread(target=migration.run).start()
                Thread(target=self.status_updater, args=(migration,)).start()

            sleep(5)

    def status_updater(self, migration: Migration):
        migration_template = Migration(migration.mount_points, migration.source, None)

        while migration.migration_state not in [MigrationState.SUCCESS, MigrationState.ERROR]:
            self.migration_pickler.update(migration_template, migration)
            sleep(5)

        self.migration_pickler.update(migration_template, migration)
