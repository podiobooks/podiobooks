"""
    This file provides translation from unstructured authors to structured authors during data migration
"""

award_translation = {
                      
                      
                      '40':  ['parsec-awards-2006-winner', ],
                      '53':  ['parsec-awards-2006-winner', ],
                      '56':  ['parsec-awards-2006-nominee', ],
                      '59':  ['parsec-awards-2006-nominee', ],
                      '61':  ['parsec-awards-2007-nominee', ],
                      '66':  ['parsec-awards-2007-nominee', ],
                      '68':  ['preditors-and-editors-awards-2005-top-ten', ],
                      '76':  ['eppie-awards-2007-winner', ],
                      '83':  ['parsec-awards-2006-winner', ],
                      '90':  ['eppie-awards-2004-winner', ],
                      '98':  ['parsec-awards-2006-nominee', ],
                      '100': ['parsec-awards-2007-nominee', ],
                      '101': ['podcast-awards-2006-nominee', ],
                      '110': ['parsec-awards-2007-nominee', ],
                      '112': ['parsec-awards-2007-nominee', ],
                      '112': ['parsec-awards-2007-nominee', ],
                      '115': ['parsec-awards-2007-nominee', ],
                      '116': ['parsec-awards-2007-nominee', ],
                      '125': ['stephen-leacock-memorial-medal-for-humor-2008', ],
                      '132': ['parsec-awards-2007-nominee', ],
                      '135': ['parsec-awards-2007-winner', ],
                      '147': ['parsec-awards-2007-winner', ],
                      '148': ['parsec-awards-2007-nominee', ],
                      '229': ['parsec-awards-2009-finalist', 'podcast-peer-awards-2008-finalist'],
                      '279': ['mark-time-awards-2007-gold-winner', ],
                      '279': ['sir-julius-vogel-awards-2009-winner', ],
                      '293': ['parsec-awards-2009-finalist', ],
                      '304': ['parsec-awards-2008-nominee', ],
                      '312': ['parsec-awards-2009-finalist', ],
                      '317': ['parsec-awards-2009-finalist', ],
                      '341': ['parsec-awards-2009-finalist', ],
                      '353': ['parsec-awards-2009-finalist', ],
                      '359': ['parsec-awards-2009-finalist', ],
                      '375': ['parsec-awards-2009-finalist', ],
                      '435': ['parsec-awards-2009-finalist', ],
                      }

def translate_award(title_id):
    try:
        award_list = award_translation[title_id]
    except:
        award_list = None
        
    return award_list
