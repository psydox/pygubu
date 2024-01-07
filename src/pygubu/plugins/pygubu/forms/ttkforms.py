import tkinter as tk
from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
    register_custom_property,
)
import pygubu.forms.ttkforms as ttkforms
import pygubu.plugins.tk.tkstdwidgets as tkw
import pygubu.plugins.ttk.ttkstdwidgets as ttkw
from pygubu.i18n import _
from pygubu.utils.datatrans import ListDTO
from pygubu.forms.fields import FieldBase
from .base import FieldBOMixin

# Groups for ordering buttons in designer palette.
GROUP0: int = 0
GROUP1: int = 10
GROUP2: int = 20
GROUP3: int = 30

_plugin_uid = "pygubu.forms.ttk"
_designer_tabs = ("ttk", _("Pygubu Forms"))
_list_dto = ListDTO()


class FrameFormBO(FieldBOMixin, ttkw.TTKFrame):
    class_ = ttkforms.FrameForm
    properties = ttkw.TTKFrame.properties + ("field_name",)
    ro_properties = ttkw.TTKFrame.ro_properties + ("field_name",)

    def add_child(self, bobject):
        if issubclass(bobject.class_, FieldBase):
            self.widget.add_field(bobject.widget)


_builder_uid = f"{_plugin_uid}.FrameForm"
register_widget(
    _builder_uid,
    FrameFormBO,
    "Form",
    _designer_tabs,
    group=GROUP0,
)


class LabelFieldInfoBO(FieldBOMixin, ttkw.TTKLabel):
    class_ = ttkforms.LabelFieldInfo
    properties = ttkw.TTKLabel.properties + ("field_name",)
    ro_properties = ttkw.TTKLabel.ro_properties + ("field_name",)


_builder_uid = f"{_plugin_uid}.LabelFieldInfo"
register_widget(
    _builder_uid,
    LabelFieldInfoBO,
    "LabelFieldInfo",
    _designer_tabs,
    group=GROUP1,
)
register_custom_property(_builder_uid, "field_name", "fieldname_selector")


class LabelFieldBO(FieldBOMixin, ttkw.TTKLabel):
    class_ = ttkforms.LabelField
    properties = ttkw.TTKLabel.properties + FieldBOMixin.base_properties
    ro_properties = ttkw.TTKLabel.ro_properties + FieldBOMixin.base_properties


_builder_uid = f"{_plugin_uid}.LabelField"
register_widget(
    _builder_uid,
    LabelFieldBO,
    "LabelField",
    _designer_tabs,
    group=GROUP2,
)


class EntryFieldBO(FieldBOMixin, ttkw.TTKEntry):
    class_ = ttkforms.EntryField
    properties = ttkw.TTKEntry.properties + FieldBOMixin.base_properties
    ro_properties = ttkw.TTKEntry.ro_properties + FieldBOMixin.base_properties


_builder_uid = f"{_plugin_uid}.EntryField"
register_widget(
    _builder_uid,
    EntryFieldBO,
    "EntryField",
    _designer_tabs,
    group=GROUP2,
)


class CheckbuttonFieldBO(FieldBOMixin, ttkw.TTKCheckbutton):
    class_ = ttkforms.CheckbuttonField
    properties = ttkw.TTKCheckbutton.properties + FieldBOMixin.base_properties
    ro_properties = (
        ttkw.TTKCheckbutton.ro_properties + FieldBOMixin.base_properties
    )


_builder_uid = f"{_plugin_uid}.CheckbuttonField"
register_widget(
    _builder_uid,
    CheckbuttonFieldBO,
    "CheckbuttonField",
    _designer_tabs,
    group=GROUP3,
)


class ComboboxFieldBO(FieldBOMixin, ttkw.TTKCombobox):
    class_ = ttkforms.ComboboxField
    properties = ttkw.TTKCombobox.properties + FieldBOMixin.base_properties
    ro_properties = (
        ttkw.TTKCombobox.ro_properties + FieldBOMixin.base_properties
    )


_builder_uid = f"{_plugin_uid}.ComboboxField"
register_widget(
    _builder_uid,
    ComboboxFieldBO,
    "ComboboxField",
    _designer_tabs,
    group=GROUP3,
)
register_custom_property(
    _builder_uid,
    "state",
    "choice",
    values=("", "normal", "disabled", "readonly"),
    state="readonly",
)


_entry_charfield_props = (
    "class_",
    "cursor",
    "takefocus",
    "style",
    "exportselection",
    "font",
    "justify",
    "show",
    "state",
    "textvariable",
    "validate",
    "width",
)

_char_field_props = (
    "max_length",
    "min_length",
    "strip",
    "empty_value",
)


class CharFieldConfigBO(BuilderObject):
    """
    Temporarly save this class as example.
    It will be converted to ConstrainConfig or something.
    """

    class_ = None
    container = False
    layout_required = False
    allow_bindings = False
    allowed_parents = (f"{_plugin_uid}.EntryField",)

    def realize(self, parent, extra_init_args: dict = None):
        self.widget = parent.get_child_master()
        return self.widget

    def configure(self, target=None):
        pass

    def layout(self, target=None):
        pass


_builder_uid = f"{_plugin_uid}.CharFieldConfig"
register_widget(
    _builder_uid,
    CharFieldConfigBO,
    "CharFieldConfig",
    _designer_tabs,
    group=999,
)
EntryFieldBO.add_allowed_child(_builder_uid)