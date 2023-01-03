import os
import shutil
import typing
from bcdd import data
import re

class Path:
    def __init__(self, path: str, is_relative: bool = False):
        if is_relative:
            self.path = self.get_relative_path(path)
        else:
            self.path = path
    
    def get_relative_path(self, path: str) -> str:
        return os.path.join(self.get_files_folder().path, path)
    
    @staticmethod
    def get_files_folder() -> "Path":
        return Path(os.path.join(os.path.dirname(os.path.abspath(__file__)), "files"))
    
    def open(self):
        self.generate_dirs()
        os.startfile(self.path)
    
    def to_str(self) -> str:
        return self.path
    
    def to_str_forwards(self) -> str:
        return self.path.replace("\\", "/")
    
    @staticmethod
    def get_appdata_folder() -> "Path":
        app_name = "bcml"
        os_name = os.name
        if os_name == "nt":
            path = Path.join(os.environ["APPDATA"], app_name)
        elif os_name == "posix":
            path = Path.join(os.environ["HOME"], app_name)
        elif os_name == "mac":
            path = Path.join(os.environ["HOME"], "Library", "Application Support", app_name)
        else:
            raise OSError("Unknown OS")
        path.generate_dirs()
        return path
    
    @staticmethod
    def get_temp_folder() -> "Path":
        return Path(os.path.join(os.environ["TEMP"], "bcml"))
        
    def generate_dirs(self: "Path") -> "Path":
        if not self.exists():
            try:
                self.__make_dirs()
            except OSError:
                pass
        return self
    
    def create(self) -> "Path":
        if not self.exists():
            self.write(data.Data())
        return self
    
    def exists(self) -> bool:
        return os.path.exists(self.path)
    
    def __make_dirs(self) -> "Path":
        os.makedirs(self.path)
        return self
    
    def basename(self) -> str:
        return os.path.basename(self.path)
    
    
    @staticmethod
    @typing.overload
    def join(*paths: str) -> "Path":
        ...
    
    @staticmethod
    @typing.overload
    def join(*paths: "Path") -> "Path":
        ...

    @staticmethod
    def join(*paths: typing.Union[str, "Path"]) -> "Path":
        _paths: list[str] = [str(path) for path in paths]
        return Path(os.path.join(*_paths))
    
    @typing.overload
    def add(self, *paths: "Path") -> "Path":
        ...
    
    @typing.overload
    def add(self, *paths: str) -> "Path":
        ...

    def add(self, *paths: typing.Union[str, "Path"]) -> "Path":
        _paths: list[str] = [str(path) for path in paths]
        return Path(os.path.join(self.path, *_paths))
    
    def __str__(self) -> str:
        return self.path
    
    def __repr__(self) -> str:
        return self.path
    
    def remove_tree(self, ignoreErrors: bool = False) -> "Path":
        if self.exists():
            shutil.rmtree(self.path, ignore_errors=ignoreErrors)
        return self
    
    def remove(self):
        if self.exists():
            os.remove(self.path)
    
    def has_files(self) -> bool:
        return len(os.listdir(self.path)) > 0
    
    def copy(self, target: "Path"):
        if self.exists():
            if self.is_directory():
                self.copy_tree(target)
            else:
                shutil.copy(self.path, target.path)
    
    def copy_tree(self, target: "Path"):
        if target.exists():
            target.remove_tree()
        if self.exists():
            shutil.copytree(self.path, target.path)
    
    def read(self, create: bool = False) -> "data.Data":
        if self.exists():
            return data.Data.from_file(self)
        elif create:
            self.write(data.Data())
            return self.read()
        else:
            raise FileNotFoundError(f"File not found: {self.path}")
            
    
    def write(self, data: "data.Data"):
        data.to_file(self)
    
    def get_files(self, regex: typing.Optional[str] = None) -> list["Path"]:
        if self.exists():
            if regex is None:
                return [self.add(file) for file in os.listdir(self.path)]
            else:
                return [self.add(file) for file in os.listdir(self.path) if re.match(regex, file)]
        return []
    
    def get_dirs(self) -> list["Path"]:
        return [file for file in self.get_files() if file.is_directory()]
    
    def is_directory(self) -> bool:
        return os.path.isdir(self.path)
    
    def change_name(self, name: str) -> "Path":
        return self.parent().add(name)
    
    def parent(self) -> "Path":
        return Path(os.path.dirname(self.path))
    
    def change_extension(self, extension: str) -> "Path":
        return Path(self.path.rsplit(".", 1)[0] + "." + extension)
    
    def remove_extension(self) -> "Path":
        return Path(self.path.rsplit(".", 1)[0])
    
    def get_extension(self) -> str:
        try:
            return self.path.rsplit(".", 1)[1]
        except IndexError:
            return ""
    
    def get_file_name(self) -> str:
        return self.path.rsplit("\\", 1)[-1]
    
    def get_file_name_without_extension(self) -> str:
        return self.get_file_name().rsplit(".", 1)[0]
    
    def get_file_size(self) -> int:
        return os.path.getsize(self.path)