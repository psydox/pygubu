import pygubu.plugins.pygubu.designer.properties
from pygubu.api.v1 import IDesignerPlugin
from pygubu.utils.widget import crop_widget
from pygubu.stockimage import StockRegistry, StockImageCache, StockImage
from .toplevelframe import ToplevelFramePreviewBO
from .basehelpers import TKTextPreviewBO


class PygubuDesignerPlugin(IDesignerPlugin):
    def get_preview_builder(self, builder_uid: str):
        if builder_uid in (
            "tk.Tk",
            "tk.Toplevel",
            "pygubu.widgets.Dialog",
            "pygubu.builder.widgets.dialog",  # This will be removed
        ):
            return ToplevelFramePreviewBO
        elif builder_uid == "tk.Text":
            return TKTextPreviewBO
        return None

    def get_toplevel_preview_for(
        self, builder_uid: str, widget_id: str, builder, top_master
    ):
        top = None
        if builder_uid == "tk.Toplevel":
            top = builder.get_object(widget_id, top_master)
        elif builder_uid == "tk.Tk":
            # for a new tk root, create a diferent image cache:
            def on_root_created(root):
                image_cache = StockImageCache(root, StockImage.registry)
                builder.image_cache = image_cache

            builder.on_first_object = on_root_created
            top = builder.get_object(widget_id)
        elif builder_uid in (
            "pygubu.widgets.Dialog",
            "pygubu.builder.widgets.dialog",
        ):
            dialog = builder.get_object(widget_id, top_master)
            dialog.run()
            top = dialog.toplevel
        return top

    def configure_for_preview(self, builder_uid: str, widget):
        """Make widget just display with minimal functionality."""
        if builder_uid.endswith(".pathchooserinput"):
            crop_widget(widget.entry)
            crop_widget(widget.folder_button)
        if builder_uid.endswith(".ColorInput"):
            crop_widget(widget._entry)
            crop_widget(widget._button)

    def ensure_visibility_in_preview(self, builder, selected_uid: str):
        """Ensure visibility of selected_uid in preview.
        Usage example:
            Activate a tab of a Notebook if the selected widget is
            inside the notebook.
        """
        xpath = ".//object[@class='ttk.Notebook.Tab']"
        # find all tabs
        tabs = builder.uidefinition.root.findall(xpath)
        if tabs is None:
            return

        for tab in tabs:
            tab_id = tab.get("id")
            # Check if this tab was clicked
            if tab_id == selected_uid:
                xpath = "./child/object[1]"
                child = tab.find(xpath)
                # A tab can be empty, check that.
                if child is not None:
                    child_id = child.get("id")
                    notebook = builder.objects[tab_id].widget
                    current_tab = builder.objects[child_id].widget
                    notebook.select(current_tab)
                    notebook.update()
                    # Found, stop searching
                    break
            # check if selected_uid is inside this tab
            xpath = f".//object[@id='{selected_uid}']"
            o = tab.find(xpath)
            if o is not None:
                # selected_uid is inside, find the tab child
                # and select this tab
                xpath = "./child/object[1]"
                child = tab.find(xpath)
                child_id = child.get("id")
                notebook = builder.objects[tab_id].widget
                current_tab = builder.objects[child_id].widget
                notebook.select(current_tab)
                notebook.update()
                # Found, stop searching
                break
