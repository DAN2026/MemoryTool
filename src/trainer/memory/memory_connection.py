import ctypes
from typing import Optional, ClassVar, Any
import pymem
import pymem.process
from loguru import logger


class MemoryConnection:
    """
    Single shared handle to the target process.

    Supports lazy attachment — the connection is optional on construction
    and can be re-established at any time via `reconnect()`.
    """

    __pm: Optional[pymem.Pymem]
    __module_base: Optional[int]
    __process_name: str
    __STILL_ACTIVE: ClassVar[int] = 259

    __slots__ = ("__pm", "__module_base", "__process_name")

    def __init__(self, process_name: str, auto_attach: bool = False) -> None:
        """
        Prepare the connection object, optionally attaching immediately.

        Args:
            process_name: The executable name, e.g. "ShooterGame.exe".
            auto_attach: If True, attempt to attach immediately.
        """
        self.__process_name: str = process_name
        self.__pm = None
        self.__module_base = None

        if auto_attach:
            self.__attach()

    def __attach(self) -> bool:
        """
        Open the process handle and resolve the module base address.

        Returns:
            True on success, False if the process was not found.
        """
        try:
            pm: pymem.Pymem = pymem.Pymem(self.__process_name)
            module: Any = pymem.process.module_from_name(
                pm.process_handle, self.__process_name
            )

            if module is None:
                logger.warning(
                    f"Module '{self.__process_name}' not found in process."
                )
                return False

            self.__pm = pm
            self.__module_base = int(module.lpBaseOfDll)

            logger.success(
                f"Attached to '{self.__process_name}' @ {hex(self.__module_base)}"
            )
            return True

        except Exception as e:
            logger.warning(f"Could not attach to '{self.__process_name}': {e}")
            return False

    def check_connection(self) -> bool:
        """
        Verifies connection by attempting to read/write to the module base.

        If the game has closed, the memory handle will fail to access the 
        base address, returning False.

        Returns:
            bool: True if memory is still accessible.
        """
        if not self.is_alive:
            return False

        try:
            self.__pm.read_char(self.__module_base)
            return True
        except Exception:
            return False

    def is_running(self) -> bool:
        """
        Checks the process exit code via WinAPI to see if it is still active.

        Returns:
            bool: True if the process is currently running (Exit Code 259).
        """
        if self.__pm is None or self.__pm.process_handle is None:
            return False

        exit_code: ctypes.c_ulong = ctypes.c_ulong()
        success: int = ctypes.windll.kernel32.GetExitCodeProcess(
            self.__pm.process_handle, ctypes.byref(exit_code)
        )

        return bool(success and exit_code.value == self.__STILL_ACTIVE)

    def reconnect(self) -> bool:
        """
        Attempt to (re-)attach to the target process.

        Returns:
            True if the connection was established, False otherwise.
        """
        self.disconnect()
        logger.info(f"Attempting to reconnect to '{self.__process_name}' …")
        return self.__attach()

    def disconnect(self) -> None:
        """
        Release the process handle and clear the module base.
        """
        if self.__pm is not None:
            try:
                self.__pm.close_process()
            except Exception:
                pass
            self.__pm = None
            self.__module_base = None
            logger.info(f"Disconnected from '{self.__process_name}'.")

    @property
    def pm(self) -> pymem.Pymem:
        """
        The active pymem.Pymem process handle.
        """
        if self.__pm is None:
            raise RuntimeError(
                f"Not connected to '{self.__process_name}'. Call reconnect()."
            )
        return self.__pm

    @property
    def module_base(self) -> int:
        """
        The base address of the process module in memory.
        """
        if self.__module_base is None:
            raise RuntimeError(
                f"Module base not resolved for '{self.__process_name}'."
            )
        return self.__module_base

    @property
    def is_alive(self) -> bool:
        """
        True if both the process handle and module base are active.
        """
        return self.__pm is not None and self.__module_base is not None

    @property
    def process_name(self) -> str:
        """
        The target executable name.
        """
        return self.__process_name