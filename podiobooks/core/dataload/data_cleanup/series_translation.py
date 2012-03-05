"""
    This file provides translation from unstructured titles to structured series during data migration
"""

SERIES_TRANSLATION = {
                      '53': '7th-son',
                      '103': '7th-son',
                      '192': '7th-son',
                      '444': '7th-son',
                      '97': 'heaven',
                      '112': 'heaven',
                      '260': 'heaven',
                      '396': 'heaven',
                      '130': 'a-traders-tale-from-the-golden-age-of-the-solar-clipper',
                      '151': 'a-traders-tale-from-the-golden-age-of-the-solar-clipper',
                      '184': 'a-traders-tale-from-the-golden-age-of-the-solar-clipper',
                      '293': 'a-traders-tale-from-the-golden-age-of-the-solar-clipper',
                      '436': 'a-traders-tale-from-the-golden-age-of-the-solar-clipper',
                      '582': 'a-traders-tale-from-the-golden-age-of-the-solar-clipper',
                      '237': 'a-shamans-tale-from-the-golden-age-of-the-solar-clipper',
                      }

def translate_series(title_id):
    """Translate from a PB1 Book ID to a PB2 Series Slug"""
    try:
        series = SERIES_TRANSLATION[title_id]
    except:
        series = None
        
    return series
