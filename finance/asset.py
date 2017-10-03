import time

from finance.snapshot import Snapshot
from finance.snapshot_history import SnapshotHistory

class Asset:

    def __init__(self, name, owner, symbol, asset_class):
        self.name = name
        self.owner = owner
        self.symbol = symbol
        self.asset_class = asset_class
        self.history = SnapshotHistory()

    def value(self, query_time=None):
        return self.history.value(query_time)

    def import_snapshot(self, time, value):
        snapshot = Snapshot(time,value)
        return self.history.import_snapshot(snapshot)
