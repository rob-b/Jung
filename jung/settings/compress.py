import os
PROJECT_DIR = os.path.dirname(os.path.realpath(os.path.join(__file__, '..')))

# compress settings
COMPRESS_CSS = {
    'all': {
        'source_filenames': ('css/reset.css', 'css/main.css'),
        'output_filename': 'all.css',
    }
}
COMPRESS_JS = {
    'all': {
        'source_filenames': ('js/jquery-1.3.2.min.js', 'js/jquery.corners.min.js',
                             'js/site.js'),
        'output_filename': 'all.js',
    }
}
CSSTIDY_BINARY = os.path.join(PROJECT_DIR, 'csstidy')
