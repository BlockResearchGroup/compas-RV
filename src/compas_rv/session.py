import datetime
import os
import pathlib
import tempfile

import compas
import compas.data
import compas.datastructures
import compas.geometry
import compas.tolerance
from compas.scene import Scene


class SessionError(Exception):
    pass


class Session:
    _instance = None
    _is_inited = False

    CONFIG = {
        "autosave.events": False,
    }

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            instance = object.__new__(cls)
            instance._is_inited = False
            cls._instance = instance
        return cls._instance

    def __init__(self, name="RhinoVAULT", basedir=None):
        if not self._is_inited:
            self.name = name
            self.data = {}
            self.current = -1
            self.depth = 53
            self.history = []
            self.timestamp = int(datetime.datetime.timestamp(datetime.datetime.now()))
            self.basedir = basedir
        self._is_inited = True

    @property
    def tempdir(self):
        if self.basedir:
            tempdir = pathlib.Path(self.basedir) / "temp"
            tempdir.mkdir(exist_ok=True)

    def __contains__(self, key):
        return key in self.data

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    def get(self, key, default=None):
        if key not in self.data:
            return default
        return self.data[key]

    def set(self, key, value):
        self.data[key] = value

    def setdefault(self, key, factory):
        if key not in self.data:
            self.set(key, factory())
        return self.get(key)

    def open(self, filepath):
        self.reset()
        self.data = compas.json_load(filepath)

    def save(self, filepath):
        compas.json_dump(self.data, filepath)

    def undo(self):
        if self.current < 0:
            print("Nothing to undo!")
            return False

        if self.current == 0:
            print("Nothing more to undo!")
            return False

        self.current -= 1
        filepath, _ = self.history[self.current]
        self.data = compas.json_load(filepath)

        return True

    def redo(self):
        if self.current == len(self.history) - 1:
            print("Nothing more to redo!")
            return False

        self.current += 1
        filepath, _ = self.history[self.current]
        self.data = compas.json_load(filepath)

        return True

    def record(self, eventname):
        if self.current > -1:
            if self.current < len(self.history) - 1:
                self.history[:] = self.history[: self.current + 1]

        fd, filepath = tempfile.mkstemp(dir=self.tempdir, suffix=".json", text=True)

        compas.json_dump(self.data, filepath)
        self.history.append((filepath, eventname))

        h = len(self.history)
        if h > self.depth:
            self.history[:] = self.history[h - self.depth :]
        self.current = len(self.history) - 1

    def reset(self):
        self.current = -1
        self.depth = 53
        for filepath, eventname in self.history:
            try:
                os.unlink(filepath)
            except PermissionError:
                pass
            except Exception:
                pass
        self.history = []

    # =============================================================================
    # Firs-class citizens
    # =============================================================================

    def scene(self, name=None):
        # type: (str | None) -> Scene
        name = name or f"{self.name}.Scene"
        scene: Scene = self.setdefault(name, factory=Scene)
        scene.name = name
        return scene
