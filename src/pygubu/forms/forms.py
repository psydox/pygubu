from .fields import Field, FieldInfoDisplay
from .exceptions import ValidationError
from .validators import EMPTY_VALUES


class BaseFormMixin:
    def __init__(
        self,
        *args,
        fname,
        empty_permitted=False,
        use_required_attribute=None,
        **kw,
    ):
        self.fname = fname
        self.empty_permitted = empty_permitted
        if use_required_attribute is not None:
            self.use_required_attribute = use_required_attribute
        self.fields = {}
        self.is_bound = False
        self._errors = None
        self._fields_scanned = False
        self._info_displays = {}
        super().__init__(*args, **kw)

    @property
    def errors(self):
        """Return an ErrorDict for the data provided for the form."""
        if self._errors is None:
            self.full_clean()
        return self._errors

    def is_valid(self):
        """Return True if the form has no errors, or False otherwise."""
        return self.is_bound and not self.errors

    def full_clean(self):
        """
        Clean all of self.data and populate self._errors and self.cleaned_data.
        """
        self._errors = {}
        if not self.is_bound:  # Stop further processing.
            return
        self.cleaned_data = {}
        # If the form is permitted to be empty, and none of the form data has
        # changed from the initial data, short circuit any validation.
        if self.empty_permitted and not self.has_changed():
            return

        self._clean_fields()
        self._clean_form()
        self._post_clean()

    def _clean_fields(self):
        for name, field in self._iter_fields():
            value = field.initial if field.disabled else field.data
            try:
                value = field.clean(value)
                self.cleaned_data[name] = value
            except ValidationError as e:
                self.add_error(name, e)
                field.mark_invalid()

    def _clean_form(self):
        try:
            cleaned_data = self.clean()
        except ValidationError as e:
            self.add_error(None, e)
        else:
            if cleaned_data is not None:
                self.cleaned_data = cleaned_data

    def _post_clean(self):
        """
        An internal hook for performing additional cleaning after form cleaning
        is complete. Used for model validation in model forms.
        """
        pass

    def clean(self):
        """
        Hook for doing any extra form-wide cleaning after Field.clean() has been
        called on every field. Any ValidationError raised by this method will
        not be associated with a particular field; it will have a special-case
        association with the field named '__all__'.
        """
        return self.cleaned_data

    def has_changed(self):
        """Return True if data differs from initial."""
        return bool(self.changed_data)

    # @cached_property
    def changed_data(self):
        return [name for name, bf in self._bound_items() if bf._has_changed()]

    def add_error(self, field, error):
        self._errors[field] = error
        if field in self._info_displays:
            self._info_displays[field].show_error(error)

    #
    # ---------
    #
    def _iter_fields(self, force_scan=False):
        if self._fields_scanned is False or force_scan:
            print("Searching for fields in iter function.")
            self._find_fields()
        for name, field in self.fields.items():
            yield name, field
        self._fields_scanned = True

    def _find_fields(self, master=None):
        if master is None:
            master = self
        for widget in master.winfo_children():
            if isinstance(widget, Field):
                self.fields[widget.fname] = widget
                print(f"Field Found: {widget.fname}")
            elif isinstance(widget, FieldInfoDisplay):
                self._info_displays[widget.fname] = widget
            else:
                self._find_fields(widget)

    def add_field(self, field):
        self.fields[field.fname] = field

    def edit(self, data: dict):
        for name, field in self._iter_fields():
            if name in data:
                field.data = data[name]
            else:
                field.data = "" if field.initial is None else field.initial
            if name in self._info_displays:
                self._info_displays[name].clear()

    def submit(self):
        self.is_bound = True
        for name in self._info_displays:
            self._info_displays[name].clear()
        self.full_clean()