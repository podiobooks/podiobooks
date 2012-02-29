"""
    This file provides translation from unstructured titles to structured series during data migration
"""

series_translation = {
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
    try:
        series = series_translation[title_id]
    except:
        series = None
        
    return series
