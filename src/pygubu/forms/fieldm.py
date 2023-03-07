"""Base clases for field data and view manipulation."""

import tkinter as tk


class FieldManager(object):
    def __init__(self, field):
        self.field = field


class FieldDataManager(FieldManager):

    # Field Widget Data Manager
    # This class will help user to customize widget data management.

    def set_value(self, value):
        # will set the value in the widget format
        raise NotImplementedError(
            f"Subclasses must define this method. {self.__class__}"
        )

    def get_value(self):
        # Get value in the widget
        raise NotImplementedError(
            f"Subclasses must define this method. {self.__class__}"
        )

    def to_python(self, value):
        # will return a python object representation of value"
        # should raise ValidationError if value can't be conveted.
        return value

    def validate(self, value):
        # field specific validation.
        # should raise ValidationError if invalid
        pass

    @property
    def data(self):
        return self.get_value()

    @data.setter
    def data(self, value):
        self.set_value(value)


class FieldViewManager(FieldManager):
    def mark_invalid(self, state: bool):
        # Visually mark the widget as invalid depending on state parameter.
        raise NotImplementedError(
            f"Subclasses must define this method. {self.__class__}"
        )

    def is_disabled(self) -> bool:
        # Asume parent class of field is a tk.Widget
        return "disabled" == self.field.cget("state")

    @property
    def disabled(self):
        return self.is_disabled()


class TkvarFDM(FieldDataManager):
    def __init__(self, *args, variable: tk.Variable, **kw):
        self.tkvar = variable
        super().__init__(*args, **kw)

    def set_value(self, value):
        self.tkvar.set(value)

    def get_value(self):
        return self.tkvar.get()
