"""
    This file provides translation from unstructured authors to structured authors during data migration
"""

contributor_translation = {
                      'jeff white': [{'name': 'Jeff White', 'type': 'Author'}, ],
                      'Mur Lafferty (editor)': [{'name': 'Mur Lafferty', 'type': 'Editor'}, ],
                      'Jeff Kafer (Editor)': [{'name': 'Jeffrey Kafer', 'type': 'Editor'}, ],
                      'Jeffrey Kafer (Editor)': [{'name': 'Jeffrey Kafer', 'type': 'Editor'}, ],
                      'Michelle M. Welch, editor': [{'name': 'Michelle M. Welch', 'type': 'Editor'}, ],
                      'Ramona Holliday, narrated by Jeffrey Kafer': [{'name': 'Ramona Holliday', 'type': 'Author'}, {'name': 'Jeffrey Kafer', 'type': 'Narrator'}, ],
                      'Stacey Cochran, narrated by Owen Daly': [{'name': 'Stacey Cochran', 'type': 'Author'}, {'name': 'Owen Daly', 'type': 'Narrator'}, ],
                      'Kabir - Interpreted by Jabez L. Van Cleef': [{'name': 'Kabir', 'type': 'Author'}, {'name': 'Jabez L. Van Cleef', 'type': 'Narrator'}, ],
                      'Jabez Van Cleef': [{'name': 'Jabez L. Van Cleef', 'type': 'Author'}, ],
                      'L. Frank Baum (read by Jason Pomerantz)': [{'name': 'L. Frank Baum', 'type': 'Author'}, {'name': 'Jason Pomerantz', 'type': 'Narrator'}, ],
                      'ThornDaddy and Dollie Llama': [{'name': 'ThornDaddy', 'type': 'Author'}, {'name': 'Dollie Llama', 'type': 'Author'}, ],
                      'Dollie Llama and ThornDaddy': [{'name': 'Dollie Llama', 'type': 'Author'}, {'name': 'ThornDaddy', 'type': 'Author'}, ],
                      'George and Weedon Grossmith': [{'name': 'George Grossmith', 'type': 'Author'}, {'name': 'Weedon Grossmith', 'type': 'Author'}, ],
                      'Mercedes Lackey and Steve Libbey': [{'name': 'Mercedes Lackey', 'type': 'Author'}, {'name': 'Steve Libbey', 'type': 'Author'}, ],
                      'Andrew Culver and Josh Charney': [{'name': 'Andrew Culver', 'type': 'Author'}, {'name': 'Josh Charney', 'type': 'Author'}, ],
                      'Linda and Morris Tannehill': [{'name': 'Linda Tannehill', 'type': 'Author'}, {'name': 'Morris Tannehill', 'type': 'Author'}, ],
                      'Billie Pagliolo': [{'name': 'Billie Pagliolo-Olmon', 'type': 'Author'}, ],
                      'MIke Bennett': [{'name': 'Mike Bennett', 'type': 'Author'}, ],
                      'Mark Yoshimoto Nemcoff (writing as Alex Damien)': [{'name': 'Mark Yoshimoto Nemcoff', 'type': 'Author'}, {'name': 'Alex Damien', 'type': 'Penname'}, ],
                      'Tee Morris (with Lisa Lee)': [{'name': 'Tee Morris', 'type': 'Author'}, {'name': 'Lisa Lee', 'type': 'Contributor'}, ],
                      'Patrick McLean': [{'name': 'Patrick E. McLean', 'type': 'Author'}, ],
                      'Compiled by Nobilis': [{'name': 'Nobilis', 'type': 'Editor'}, ],
                      'John Stockmyer': [{'name': 'John G. Stockmyer', 'type': 'Author'}, ],
                      'A Square (Edwin Abbott Abbott)': [{'name': 'Edwin Abbott Abbott', 'type': 'Author'}, {'name': 'A Square', 'type': 'Penname'}, ],
                      'John C. Adler, Ph.D., as told to Bill DeSmedt': [{'name': 'John C. Adler, Ph.D.', 'type': 'Author'}, {'name': 'Bill DeSmedt', 'type': 'Ghostwriter'}, ],
                      'Jeremy Robinson': [{'name': 'Jeremy Robinson', 'type': 'Author'}, {'name': 'Jeffrey Kafer', 'type': 'Narrator'}, ],
                      'Mike Yachnik': [{'name': 'Mike Yachnik', 'type': 'Author'}, {'name': 'Jeffrey Kafer', 'type': 'Narrator'}, ],
                      'J. J. Hebert': [{'name': 'J.J. Hebert', 'type': 'Author'}, {'name': 'Jeffrey Kafer', 'type': 'Narrator'}, ],
                      }

def translate_contributor(legacy_display_name):
    try:
        translated_name = contributor_translation[legacy_display_name]
    except:
        translated_name = [{'name': legacy_display_name, 'type': 'Author' }, ]
        
    return translated_name
