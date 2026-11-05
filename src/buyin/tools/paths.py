import sys
from pathlib import Path


def desktop_folder() -> Path:
    """The user's real Desktop folder (on Windows this follows OneDrive redirection)."""
    if sys.platform == "win32":
        import ctypes

        CSIDL_DESKTOPDIRECTORY = 0x0010
        buffer = ctypes.create_unicode_buffer(260)
        if ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_DESKTOPDIRECTORY, None, 0, buffer) == 0:
            return Path(buffer.value)
    return Path.home() / "Desktop"
