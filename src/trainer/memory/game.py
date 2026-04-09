import atexit
import time
import threading
import psutil
from typing import ClassVar, Optional, Any
from loguru import logger

from trainer.memory.memory_connection import MemoryConnection
from trainer.values.fov import FovValue
from trainer.values.prevviewmode import PrevviewmodeValue
from trainer.values.mipbias import MipbiasValue
from trainer.values.environment import EnvironmentValue
from trainer.values.testingini import TestingtINI
from trainer.values.beer import BeerValue
from trainer.values.gamma import GammaValue
from trainer.values.viewdistance import ViewDistanceValue
from trainer.values.fullbright import FullbrightValue

from trainer.events.signals import (
    set_ini,
    set_fov,
    set_environment,
    set_beer,
    set_mipbias,
    set_testing_ini,
    on_connection_change,
    request_reconnect,
    request_shutdown,
    set_gamma,
    get_gamma,
    get_fov,
    set_view_distance,
    get_view_distance,
    set_fullbright,
)


class ShooterGame:
    """
    Manages the live game state. Connection is handled via explicit signals and initialization.
    A background watchdog thread detects when the process closes and notifies listeners.
    """

    __PROCESS_NAME: ClassVar[str] = "ShooterGame.exe"
    __MIN_UPTIME: ClassVar[float] = 2
    __POLL_INTERVAL: ClassVar[float] = 2.0

    ENV_ENABLED: ClassVar[float] = 28896107
    ENV_DISABLED: ClassVar[float] = 33549163
    BEER_ENABLED: ClassVar[float] = 3961701783
    BEER_DISABLED: ClassVar[float] = 3961701788
    FULLBRIGHT_ENABLED: ClassVar[float] = 3769923517
    FULLBRIGHT_DISABLED: ClassVar[float] = 3769923518
    
    __slots__ = (
        "_conn",
        "fov",
        "ini",
        "mipbias",
        "testing_ini",
        "environment",
        "beer",
        "gamma",
        "viewdistance",
        "fullbright",
        "_watchdog_thread",
        "_watchdog_stop",
        "__weakref__",
    )

    def __init__(self) -> None:
        """
        Initializes the memory connection and attempts an initial attachment.
        """
        self._conn: MemoryConnection = MemoryConnection(self.__PROCESS_NAME, auto_attach=False)

        self.fov: FovValue = FovValue(self._conn)
        self.ini: PrevviewmodeValue = PrevviewmodeValue(self._conn)
        self.mipbias: MipbiasValue = MipbiasValue(self._conn)
        self.testing_ini: TestingtINI = TestingtINI(self._conn)
        self.environment: EnvironmentValue = EnvironmentValue(self._conn)
        self.beer: BeerValue = BeerValue(self._conn)
        self.gamma: GammaValue = GammaValue(self._conn)
        self.viewdistance: ViewDistanceValue = ViewDistanceValue(self._conn)
        self.fullbright: FullbrightValue = FullbrightValue(self._conn)

        self._watchdog_thread: Optional[threading.Thread] = None
        self._watchdog_stop: threading.Event = threading.Event()

        atexit.register(self._stop_watchdog)
        self.__register_signals()
        self.reconnect()

    def __register_signals(self) -> None:
        """
        Subscribes internal handlers to global event signals.
        """
        set_ini.connect(self._set_ini)
        set_fov.connect(self._set_fov)
        set_environment.connect(self._set_environment)
        set_beer.connect(self._set_beer)
        set_mipbias.connect(self._set_mipbias)
        set_testing_ini.connect(self._set_testing_ini)
        set_gamma.connect(self._set_gamma)
        set_view_distance.connect(self._set_view_distance)
        set_fullbright.connect(self._set_fullbright)
        
        get_fov.connect(self._get_fov)
        get_gamma.connect(self._get_gamma)
        get_view_distance.connect(self._get_view_distance)
        
        request_reconnect.connect(self._reconnect_request)
        request_shutdown.connect(self._on_shutdown)

    def _start_watchdog(self) -> None:
        """
        Spawns a daemon thread that polls the connection and fires
        on_connection_change(connected=False) the moment the process dies.
        """
        self._watchdog_stop.clear()
        self._watchdog_thread = threading.Thread(
            target=self._watchdog_loop,
            name="ShooterGame-Watchdog",
            daemon=True,
        )
        self._watchdog_thread.start()
        logger.debug("Watchdog started.")

    def _stop_watchdog(self) -> None:
        """
        Signals the watchdog thread to exit without blocking the caller.
        """
        self._watchdog_stop.set()
        self._watchdog_thread = None
        logger.debug("Watchdog stop requested.")

    def _watchdog_loop(self) -> None:
        """
        Polls the memory connection every __POLL_INTERVAL seconds.
        Broadcasts a disconnect signal and exits as soon as the process is gone.
        """
        while not self._watchdog_stop.wait(self.__POLL_INTERVAL):
            if not self._conn.check_connection():
                logger.warning("Watchdog: process lost — broadcasting disconnect.")
                self._conn.disconnect()
                on_connection_change.send(self, connected=False)
                break
        logger.debug("Watchdog exited.")

    def reconnect(self) -> bool:
        """
        Stops any active watchdog, attempts a fresh connection, and
        restarts the watchdog on success.
        """
        self._stop_watchdog()

        if not self.__is_process_ready():
            on_connection_change.send(self, connected=False)
            return False

        success: bool = self._conn.reconnect()
        on_connection_change.send(self, connected=success)

        if success:
            self._start_watchdog()

        return success

    def disconnect(self) -> None:
        """
        Stops the watchdog, closes active handles, and notifies listeners.
        """
        self._stop_watchdog()
        self._conn.disconnect()
        on_connection_change.send(self, connected=False)

    @property
    def is_connected(self) -> bool:
        """
        Returns True if the memory connection is active.
        """
        return self._conn.is_alive

    def __is_process_ready(self) -> bool:
        """
        Validates that ShooterGame.exe is running and older than the threshold.
        """
        for proc in psutil.process_iter(['name', 'create_time']):
            try:
                if proc.info['name'] == self.__PROCESS_NAME:
                    uptime: float = time.time() - proc.info['create_time']

                    if uptime < self.__MIN_UPTIME:
                        logger.warning(
                            f"Connection rejected. Process only open for {uptime:.2f}s "
                            f"(Requires {self.__MIN_UPTIME}s)."
                        )
                        return False
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return False

    def _on_shutdown(self, sender: Any, **kwargs: Any) -> None:
        """
        Disconnects cleanly on shutdown — watchdog is handled by atexit.
        """
        logger.info("Shutdown requested.")
        self._conn.disconnect()

    def _reconnect_request(self, sender: Any, **kwargs: Any) -> None:
        self.reconnect()

    def _set_ini(self, sender: Any, value: int, **kwargs: Any) -> None:
        self.ini.set(value)

    def _set_fov(self, sender: Any, value: float, **kwargs: Any) -> None:
        self.fov.set(value)

    def _set_environment(self, sender: Any, state: bool, **kwargs: Any) -> None:
        val: float = self.ENV_ENABLED if state else self.ENV_DISABLED
        self.environment.set(val)

    def _set_beer(self, sender: Any, state: bool, **kwargs: Any) -> None:
        val: float = self.BEER_ENABLED if state else self.BEER_DISABLED
        self.beer.set(val)
        
    def _set_fullbright(self, sender: Any, state: bool, **kwargs: Any) -> None:
        val: float = self.FULLBRIGHT_ENABLED if state else self.FULLBRIGHT_DISABLED
        self.fullbright.set(val)
        
    def _set_mipbias(self, sender: Any, value: float, **kwargs: Any) -> None:
        self.mipbias.set(value)

    def _set_testing_ini(self, sender: Any, value: float, **kwargs: Any) -> None:
        self.testing_ini.set(value)
        
    def _set_gamma(self, sender: Any, value: float, **kwargs: Any) -> None:
        self.gamma.set(value)
        
    def _set_view_distance(self, sender: Any, value: float, **kwargs: Any) -> None:
        self.viewdistance.set(value)
        
    def _get_fov(self, sender: Any, **kwargs: Any) -> float:
        
        return self.fov.get()
            
    def _get_gamma(self, sender: Any, **kwargs: Any) -> float:
        return self.gamma.get()
    
    def _get_view_distance(self, sender: Any, **kwargs: Any) -> None:
        return self.viewdistance.get()