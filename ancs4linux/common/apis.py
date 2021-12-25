import json
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, List, cast

from ancs4linux.common.dbus import Int32, SessionBus, Str, SystemBus, UInt32, Variant

Signal = Any


@dataclass
class ShowNotificationData:
    device_address: str
    device_name: str
    appID: str
    appName: str
    id: int
    title: str
    body: str

    def json(self) -> str:
        return json.dumps(vars(self))

    @classmethod
    def parse(cls, data: str) -> "ShowNotificationData":
        return cls(**json.loads(data))


class ObserverAPI(ABC):
    def register(self) -> None:
        SystemBus().publish_object("/", self)

    @classmethod
    def connect(cls, observer_dbus: str) -> "ObserverAPI":
        return cast(ObserverAPI, SystemBus().get_proxy(observer_dbus, "/"))

    def emit_show_notification(self, data: ShowNotificationData) -> None:
        self.ShowNotification(data.json())

    ShowNotification: Signal

    def emit_dismiss_notification(self, id: int) -> None:
        self.DismissNotification(UInt32(id))

    DismissNotification: Signal


class AdvertisingAPI(ABC):
    def register(self) -> None:
        SystemBus().publish_object("/", self)

    @classmethod
    def connect(cls, advertising_dbus: str) -> "AdvertisingAPI":
        return cast(AdvertisingAPI, SystemBus().get_proxy(advertising_dbus, "/"))

    @abstractmethod
    def GetAllHci(self) -> List[Str]:
        pass

    @abstractmethod
    def EnableAdvertising(self, hci_address: Str, name: Str) -> None:
        pass

    @abstractmethod
    def DisableAdvertising(self, hci_address: Str) -> None:
        pass

    @abstractmethod
    def EnablePairing(self) -> None:
        pass

    @abstractmethod
    def DisablePairing(self) -> None:
        pass

    def emit_pairing_code(self, pin: str) -> None:
        self.PairingCode(pin)

    PairingCode: Signal


class NotificationAPI(ABC):
    """https://specifications.freedesktop.org/notification-spec/notification-spec-latest.html"""

    @classmethod
    def connect(cls) -> "NotificationAPI":
        return cast(
            NotificationAPI,
            SessionBus().get_proxy(
                "org.freedesktop.Notifications", "/org/freedesktop/Notifications"
            ),
        )

    @abstractmethod
    def Notify(
        self,
        app_name: Str,
        replaces_id: UInt32,
        app_icon: Str,
        summary: Str,
        body: Str,
        actions: List[Str],
        hints: List[Variant],
        expire_timeout: Int32,
    ) -> UInt32:
        pass

    @abstractmethod
    def CloseNotification(self, id: UInt32) -> None:
        pass
