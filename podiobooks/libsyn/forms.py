"""Forms for the Podiobooks Libsyn Module"""

from django import forms


class LibsynImportForm(forms.Form):
    """ Form used to allow input of libsyn slug to pull feed """
    libsyn_slug = forms.TextInput()
