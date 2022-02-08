from gi.repository import Gtk, GLib


class Module(Gtk.Frame):
    def __init__(self, module_widget, gtk_orientation: Gtk.Orientation) -> None:
        super().__init__()
        self.module_widget = module_widget
        self.add(self.module_widget)
        self.gtk_orientation = gtk_orientation

    def _update(self):
        raise NotImplementedError()

    def get_popover_menubutton(self, modal_widget: Gtk.Widget):
        self.popover = Gtk.Popover()
        button = Gtk.MenuButton(popover=self.popover)
        self.popover.add(modal_widget)
        self.modal_widget = modal_widget
        modal_widget.show_all()

        return button

    @staticmethod
    def __remove_button_frame__(button):
        button_style_context = button.get_style_context()
        button_style_context.add_class("module-button")


class ModuleWithModal(Module):
    def __init__(
        self, module_widget, modal_widget, gtk_orientation: Gtk.Orientation
    ) -> None:
        self.popover = Gtk.Popover()
        button = Gtk.MenuButton(popover=self.popover)
        Module.__remove_button_frame__(button)
        button.add(module_widget)
        super().__init__(module_widget=button, gtk_orientation=gtk_orientation)
        self.popover.add(modal_widget)
        modal_widget.show_all()
        self.module_widget = module_widget
        self.modal_widget = modal_widget

    def _update_modal(self):
        raise NotImplementedError()
