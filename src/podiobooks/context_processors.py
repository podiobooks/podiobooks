from settings import MEDIA_ROOT,MAIN_TEMPLATE_THEME
import hashlib
import os
import glob

def mini_css(request):
    css_files = filter(lambda x: x.endswith('.css'), os.listdir(MEDIA_ROOT + 'themes/' + MAIN_TEMPLATE_THEME + '/css/'))
    
    latest_mod = 0
    p = MEDIA_ROOT + 'themes/' + MAIN_TEMPLATE_THEME + '/css/'
    
    for css in css_files:
        if os.path.getmtime(p + css) > latest_mod:
            latest_mod = os.path.getmtime(p + css)
    latest_mod = hashlib.md5(latest_mod.__str__()).hexdigest()
    cache_name = 'style-' + latest_mod + '_.css'
    
    if not os.path.isfile(p + 'cache/' + cache_name):
        filelist = glob.glob(p + 'cache/style-*_.css')
        for file in filelist:
            os.unlink(file)
        
        css_str = ''
        try:
            f = open(p + "clear.css")
            css_str += "\n\n\n/* From: " + css + "*/\n"
            css_str += f.read()
            f.close()
        except:
            pass
        for css in css_files:
            if not css=='clear.css':
                f = open(p + css)
                css_str += "\n\n\n/* From: " + css + "*/\n"
                css_str += f.read()
                f.close()
        f = open(p + 'cache/' + cache_name,'w')
        css_str = css_str.replace('url(','url(../')
        css_str = css_str.replace('url (','url(../')
        f.write(css_str)
        f.close()
    
    return {'MINI_CSS' : 'themes/' + MAIN_TEMPLATE_THEME + '/css/cache/' + cache_name }