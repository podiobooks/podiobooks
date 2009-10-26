update main_title set license_id = main_license.id
from main_license
where main_title.license = main_license.slug;