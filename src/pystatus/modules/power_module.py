import logging
from gi.repository import Gtk
from pystatus.module import Module
from dbus_next.aio.message_bus import MessageBus
from dbus_next.constants import BusType
from dbus_next.errors import DBusError
from pystatus.utils.notifications import notify_error
from pystatus.utils.power_utils import (
    shutdown,
    restart,
    suspend_disk,
    suspend_mem,
    suspend_freeze,
)


class PowerModule(Module):
    def __init__(
        self,
        **kwargs,
    ) -> None:

        self.modal_widget = PowerModalWidget()
        modal_menubutton = self.get_popover_menubutton(self.modal_widget)
        self.module_widget = PowerWidget(modal_menubutton)

        super().__init__(module_widget=self.module_widget, **kwargs)

    def _update(self) -> bool:
        return True

    def _update_modal(self) -> bool:
        return True


class PowerWidget(Gtk.Box):
    def __init__(self, modal_menubutton):
        super().__init__()

        self.set_hexpand(True)
        self.set_vexpand(True)

        self.menubutton = modal_menubutton
        menubutton_image = Gtk.Image.new_from_icon_name(
            "system-shutdown-symbolic", Gtk.IconSize.SMALL_TOOLBAR
        )
        self.menubutton.set_image(menubutton_image)
        Module.__remove_button_frame__(self.menubutton)
        self.menubutton.set_relief(Gtk.ReliefStyle.NONE)

        self.set_center_widget(self.menubutton)


class PowerModalWidget(Gtk.Box):
    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        self.shutdown_button = Gtk.Button.new_with_label("Shutdown")
        self.shutdown_button.connect("clicked", lambda _: self.verify_action(shutdown))
        self.suspend_mem_button = Gtk.Button.new_with_label("Suspend (mem)")
        self.suspend_mem_button.connect(
            "clicked", lambda _: self.verify_action(suspend_mem)
        )
        self.suspend_freeze_button = Gtk.Button.new_with_label("Suspend (freeze)")
        self.suspend_freeze_button.connect(
            "clicked", lambda _: self.verify_action(suspend_freeze)
        )
        self.suspend_disk_button = Gtk.Button.new_with_label("Suspend (disk)")
        self.suspend_disk_button.connect(
            "clicked", lambda _: self.verify_action(suspend_disk)
        )
        self.restart_button = Gtk.Button.new_with_label("Restart")
        self.restart_button.connect("clicked", lambda _: self.verify_action(restart))

        self.add(self.suspend_freeze_button)
        self.add(self.suspend_mem_button)
        self.add(self.suspend_disk_button)
        self.add(self.restart_button)
        self.add(self.shutdown_button)

    def verify_action(self, action):
        dialog = ConfirmDialog(self.get_toplevel())
        response = dialog.run()
        dialog.destroy()

        if response == Gtk.ResponseType.YES:
            action()


class ConfirmDialog(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="Confirmation", transient_for=parent, flags=0)
        self.set_resizable(False)
        self.add_buttons(
            Gtk.STOCK_NO, Gtk.ResponseType.NO, Gtk.STOCK_YES, Gtk.ResponseType.YES
        )
        self.set_default_size(150, 100)
        label = Gtk.Label(label=f"Are you sure?")
        box = self.get_content_area()
        box.add(label)
        self.show_all()
