"""
##############################################
########-----Flatpages Importer-----##########
##############################################
"""

from django.contrib.flatpages.models import FlatPage
from django.conf import settings
from django.contrib.sites.models import Site

def import_flat_pages():
    """Imports a list of .html files into the FlatPage model"""
    
    FLATPAGE_DIR = settings.DATALOAD_DIR + '../flatpages/'
    
    ## PRE CLEANOUT
    FlatPage.objects.all().delete()
    
    ## START IMPORTING PAGES!
    
    donate_file = open(FLATPAGE_DIR + 'why_donate.html')
    donate_content = donate_file.read()
    donate_page = FlatPage.objects.create(
        url='/donate/',
        title='Donate',
        content=donate_content
    )
    donate_page.sites.add(Site.objects.get_current())
    
    authors_file = open(FLATPAGE_DIR + 'submit_your_book.html')
    authors_content = authors_file.read()
    authors_page = FlatPage.objects.create(
        url='/authors/',
        title='Authors',
        content=authors_content
    )
    authors_page.sites.add(Site.objects.get_current())
    
    staff_file = open(FLATPAGE_DIR + 'staff.html')
    staff_content = staff_file.read()
    staff_page = FlatPage.objects.create(
        url='/staff/',
        title='Staff',
        content=staff_content
    )
    staff_page.sites.add(Site.objects.get_current())
    
    
    ## HOW DID WE DO?
    for page in FlatPage.objects.all():
        print page.url
        print page.content
    
    
##### MAIN FUNCTION TO RUN IF THIS SCRIPT IS CALLED ALONE ###
if __name__ == "__main__":
    import_flat_pages()


### Handy Mapping Reference
# url = models.CharField(_('URL'), max_length=100, db_index=True)
# title = models.CharField(_('title'), max_length=200)
# content = models.TextField(_('content'), blank=True)
# enable_comments = models.BooleanField(_('enable comments'))
# template_name = models.CharField(_('template name'), max_length=70, blank=True,
#    help_text=_("Example: 'flatpages/contact_page.html'. If this isn't provided, the system will use 'flatpages/default.html'."))
# registration_required = models.BooleanField(_('registration required'), help_text=_("If this is checked, only logged-in users will be able to view the page."))
# sites = models.ManyToManyField(Site)