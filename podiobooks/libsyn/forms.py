"""Forms for the Podiobooks Libsyn Module"""

from django import forms

# pylint: disable=R0924

class LibsynImportForm(forms.Form):
    """ Form used to allow input of libsyn slug to pull feed """
    libsyn_slug = forms.CharField()
