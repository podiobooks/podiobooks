from PIL import Image
import os.path
import StringIO

def thumbnail(filename, size=(50, 50), output_filename=None):
    image = Image.open(filename)
    if image.mode not in ('L', 'RGB'):
        image = image.convert('RGB')
    image = image.resize(size, Image.ANTIALIAS)

    # get the thumbnail data in memory.
    if not output_filename:
        output_filename = get_default_thumbnail_filename(filename)
    image.save(output_filename, image.format) 
    return output_filename

def thumbnail_string(buf, size=(50, 50)):
    f = StringIO.StringIO(buf)
    image = Image.open(f)
    if image.mode not in ('L', 'RGB'):
        image = image.convert('RGB')
    image = image.resize(size, Image.ANTIALIAS)
    o = StringIO.StringIO()
    image.save(o, "JPEG")
    return o.getvalue()
    
def get_default_thumbnail_filename(filename):
    path, ext = os.path.splitext(filename)
    return path + '.thumb.jpg'
