from typing import Callable, Optional
from gi.repository import Gtk, GLib

from pystatus.config import ModuleConfig


class Module(Gtk.Box):
    def __init__(
        self,
        gtk_orientation: Gtk.Orientation,
        toggle_modal: Callable,
        config: ModuleConfig,
        bar_width: int,
        module_widget: Optional[Gtk.Widget] = None,
    ) -> None:
        super().__init__(orientation=gtk_orientation)
        self.gtk_orientation = gtk_orientation
        self.toggle_modal = toggle_modal
        self.bar_width = bar_width
        self.config = config
        if self.config.show_label:
            self.add(Gtk.Label(label=self.config.label))
        if module_widget:
            self.set_module_widget(module_widget)

    def _update(self):
        raise NotImplementedError()

    def set_module_widget(self, module_widget):
        self.module_widget = module_widget
        self.add(self.module_widget)

    def get_popover_menubutton(self, modal_widget: Gtk.Widget):
        self.modal_widget = modal_widget
        button = Gtk.Button()
        button.connect("clicked", lambda _: self.toggle_modal(self.modal_widget))
        modal_widget.show_all()

        return button

    @staticmethod
    def __remove_button_frame__(button):
        button_style_context = button.get_style_context()
        button_style_context.add_class("module-button")


class ModuleWithModal(Module):
    def __init__(
        self,
        module_widget: Gtk.Widget,
        modal_widget: Gtk.Widget,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        button = self.get_popover_menubutton(modal_widget)
        Module.__remove_button_frame__(button)
        button.add(module_widget)
        self.set_module_widget(button)
        self.module_widget = module_widget

    def _update_modal(self):
        raise NotImplementedError()
