from typing import Any, Optional
from bcdd import path, color
import requests
import subprocess

class Updater:
    def __init__(self):
        self.package_name = "bcdd"
    
    def get_installed_version(self) -> str:
        return path.Path("version.txt", True).read().to_str()
    
    def get_version_info(self) -> Optional[tuple[str, Optional[str]]]:
        try:
            response = requests.get(f"https://pypi.org/pypi/{self.package_name}/json")
            response.raise_for_status()
        except requests.exceptions.RequestException:
            return None
        data = response.json()
        info = (
            self.get_pypi_version(data),
            self.get_latest_prerelease_version(data),
        )
        return info
    
    def get_pypi_version(self, data: dict[str, Any]) -> str:
        return data["info"]["version"]

    def get_latest_prerelease_version(self, data: dict[str, Any]) -> Optional[str]:
        releases = list(data["releases"])
        releases.reverse()
        for release in releases:
            if "b" in release:
                return release
        return None
    
    def is_pypi_newer(self, local: str, pypi: Optional[str], remove_b: bool = True):
        if pypi is None:
            return False
        if remove_b:
            if "b" in pypi:
                pypi = pypi.split("b")[0]
            if "b" in local:
                local = local.split("b")[0]
        return pypi > local
    
    def check_update_data(self, version_info: Optional[tuple[str, Optional[str]]]):
        local_version = self.get_installed_version()
        if version_info is None:
            color.ColoredText().display("Could not check for updates.")
            return
        pypi_version, prerelease_version = version_info
        check_pre = "b" in local_version
        if check_pre and self.is_pypi_newer(local_version, prerelease_version, False):
            color.ColoredText().display(f"New prerelease version available: <green>{prerelease_version}</>")
            return True, prerelease_version
        if self.is_pypi_newer(local_version, pypi_version):
            color.ColoredText().display(f"New version available: <green>{pypi_version}</>")
            return True, pypi_version
        color.ColoredText().display("No updates available.")
        return False, local_version

    def check_update(self) -> bool:
        version_info = self.get_version_info()
        update_data = self.check_update_data(version_info)
        if update_data is None:
            return False
        update_available, version = update_data
        if update_available and version is not None:
            update = color.ColoredInput().get_bool("\nA new version is available. Do you want to update? <green>[y/n]</>:")
            if update:
                self.try_update(version)
                return True
        return False
            
    def try_update(self, version: str):
        commands: list[str] = ["py -m pip", "python -m pip", "python3 -m pip", "pip", "pip3"]
        for command in commands:
            success = self.update(version, command)
            if success:
                color.ColoredText().display(f"Successfully updated {self.package_name}.")
                return
        color.ColoredText().display(f"Could not update {self.package_name}. Please update manually.")
    
    def update(self, version: str, command: str) -> bool:
        full_cmd = f"{command} install -U {self.package_name}=={version}"
        try:
            subprocess.run(full_cmd, shell=True, check=True, capture_output=True)
        except subprocess.CalledProcessError:
            return False
        return True
