"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.conf import settings
from django.http import HttpRequest


from mediabrute.util import dirs, api_helpers, defaults
from mediabrute import api
from mediabrute.util import list_css_top_files, list_css_bottom_files
from mediabrute.context_processors import heavy_lifting

import os
import inspect

class CssOrderingTestCase(TestCase):
    """
    Tests relating to the proper ordering of CSS sheets
    """
    def setUp(self):
        """
        Setup for css ordering tests
        """
        self.fakeFileList = [
                             "/asdfs/gggg/yoyo/mobile.css",
                             "/asdf/gggg/yoyo2/mobile.css",
                             "/yayay/asdf/not/style.css",
                             "/hoooboy/yup.css",
                             "/ohyayay/reset.css",
                             ]
        
    def testCssTopFilesBelong(self):
        """
        Make sure that all top files returned by the organize_css_files belong there
        """
        top, std, bottom = heavy_lifting.organize_css_files(self.fakeFileList)
        for fle in top:
            self.assertIn(os.path.basename(fle), list_css_top_files())
            
    def testCssBottomFilesBelong(self):
        """
        Make sure that all bottom files returned by the organize_css_files belong there
        """
        top, std, bottom = heavy_lifting.organize_css_files(self.fakeFileList)
        for fle in bottom:
            self.assertIn(os.path.basename(fle), list_css_bottom_files())
            
    def testCssBottomFilesOrdered(self):
        """
        Make sure that the
        
        This is only important if there are multiple
        settings.CSS_BOTTOM_FILES and matches found 
        
        TODO:Finish this test
        """
        
        top, std, bottom = heavy_lifting.organize_css_files(self.fakeFileList)
         
        if len(bottom) > 1 and len(list_css_bottom_files()) > 1:
            for found_file in bottom:
                found_file_name = os.path.basename(found_file)
                
                        
                for f_file_again in bottom:
                    f_file_again_name = os.path.basename(f_file_again)
                            
                    if not found_file_name == f_file_again_name:
                        if bottom.index(found_file) > bottom.index(f_file_again):
                            self.assertGreater(list_css_bottom_files().index(found_file_name), list_css_bottom_files().index(f_file_again_name))

                        if bottom.index(found_file) < bottom.index(f_file_again):
                            self.assertLess(list_css_bottom_files().index(found_file_name), list_css_bottom_files().index(f_file_again_name))
                
                
    def testCssTopFilesOrdered(self):
        """
        Make sure that the
        
        This is only important if there are multiple
        settings.CSS_TOP_FILES and matches found
        
        TODO:Finish this test 
        """
        
        top, std, bottom = heavy_lifting.organize_css_files(self.fakeFileList)
        
        if len(top) > 1 and len(list_css_top_files()) > 1:
            for found_file in top:
                found_file_name = os.path.basename(found_file)
                
                        
                for f_file_again in top:
                    f_file_again_name = os.path.basename(f_file_again)
                            
                    if not found_file_name == f_file_again_name:
                        if top.index(found_file) > top.index(f_file_again):
                            self.assertGreater(list_css_top_files().index(found_file_name), list_css_top_files().index(f_file_again_name))

                        if top.index(found_file) < top.index(f_file_again):
                            self.assertLess(list_css_top_files().index(found_file_name), list_css_top_files().index(f_file_again_name))
                        
                                    
        

class PublicApiTestCase(TestCase):
    """
    Tests relating to mediabrute.api
    """
    
        
    def testParameterlessCalls(self):
        """
        find and call all API functions
        that require no arguments
        """
        for attr in dir(api):
            func = getattr(api, attr)
            if callable(func):                
                spec = inspect.getargspec(func)
                if not spec.args and not spec.varargs and not spec.keywords and not spec.defaults:
                    func()
                    
    
        
class DefaultSettingsTestCase(TestCase):
    """
    Test cases for default settings
    """

    def testCssDir(self):
        """
        Main CSS directory default setting test
        
        should match either settings.CSS_DIR or just "css"
        Test that it works as a fullpath AND standalone
        """
        fullpath = dirs.get_main_css_dir()
        ext_only = dirs.get_main_css_dir(full_path=False)
        
        try:
            ext_compare = settings.CSS_DIR
        except AttributeError:
            ext_compare = defaults.CSS_DIR
            
        fullpath_compare = os.path.join(settings.MEDIA_ROOT, ext_compare)
        
        self.assertEquals(fullpath_compare, fullpath)
        self.assertEquals(ext_compare, ext_only)
        
    def testJsDir(self):
        """
        Main JS directory default setting test
        
        should match either settings.JS_DIR or just "js"
        Test that it works as a fullpath AND standalone
        """
        fullpath = dirs.get_main_js_dir()
        ext_only = dirs.get_main_js_dir(full_path=False)
        
        try:
            ext_compare = settings.JS_DIR
        except AttributeError:
            ext_compare = defaults.JS_DIR
            
        fullpath_compare = os.path.join(settings.MEDIA_ROOT, ext_compare)
        
        self.assertEquals(fullpath_compare, fullpath)
        self.assertEquals(ext_compare, ext_only)
        
    def testCssTopFilesList(self):
        """
        Make sure that list_css_top_files matches 
        either settings.CSS_TOP_FILES or an empty list
        """
        try:
            self.assertEquals(settings.CSS_TOP_FILES, list_css_top_files())
        except AttributeError:
            self.assertEquals([], list_css_top_files())
    
    def testCssBottomFilesList(self):
        """
        Make sure that list_css_bottom_files matches 
        either settings.CSS_BOTTOM_FILES or an empty list
        """
        try:
            self.assertEquals(settings.CSS_BOTTOM_FILES, list_css_bottom_files())
        except AttributeError:
            self.assertEquals([], list_css_bottom_files())
            
    def testCssAppDirs(self):
        """
        First, look for an APP_CSS setting,
        otherwise, default to "css"
        """
        try:
            ext = settings.APP_CSS
        except AttributeError:
            ext = defaults.APP_CSS
        
        for app, directory in dirs.APP_CSS_DIRS:
            self.assertIn("/%s" % ext, directory)
    
    def testClearCache(self):
        """
        Test that clearing the cache works
        i.e. does not raise an error
        """
        api_helpers.clear_cache()
        
       
    def testJsAppDirs(self):
        """
        First, look for an APP_JS setting,
        otherwise, default to "js"
        """
        try:
            ext = settings.APP_JS
        except AttributeError:
            ext = defaults.APP_JS
        
        for app, directory in dirs.APP_JS_DIRS:
            self.assertIn("/%s" % ext, directory)