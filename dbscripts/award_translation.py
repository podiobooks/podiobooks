"""
    This file provides translation from unstructured authors to structured authors during data migration
"""

award_translation = {
                      
                      '53':  ['parsec-awards-2006-winner',],
                      '103': ['parsec-awards-2007-nominee',],
                      '132': ['parsec-awards-2007-nominee',],
                      '116': ['parsec-awards-2007-nominee',],
                      '101': ['podcast-awards-2006-nominee',],
                      '304': ['parsec-awards-2008-nominee',],
                      '40':  ['parsec-awards-2006-winner',],
                      '279': ['sir-julius-vogel-awards-2009-winner',],
                      }

def translate_award(title_id):
    try:
        award_list = award_translation[title_id]
    except:
        award_list = None
        
    return award_list