import os
import sys
import inspect
import xml.etree.cElementTree as ET
from collections import OrderedDict

from ckan.common import json
from ckan.lib.cli import CkanCommand


class Citation(CkanCommand):
    '''Citation commands

    Usage:

      citation build_styles
        - Generates a list of citation styles.
          By default, the following styles will be shown first:
          apa, modern-language-association, chicago-note-bibliography,
          chicago-author-date, and ieee.
    '''

    summary = __doc__.split('\n')[0]
    usage = __doc__
    max_args = 1
    min_args = 0
    m = __import__('ckanext.citation', fromlist=[''])
    p = os.path.join(
            os.path.dirname(inspect.getfile(m)),
            'public', 'ckanext', 'citation', 'csl')
    csl_p = os.path.join(p, 'styles')

    def command(self):
        if len(self.args) == 0:
            self.parser.print_usage()
            sys.exit(1)
        cmd = self.args[0]
        if cmd == 'build_styles':
            major_styles = [
                    'apa',
                    'modern-language-association',
                    'chicago-note-bibliography',
                    'chicago-author-date',
                    'ieee',
                    'council-of-science-editors',
                    'american-medical-association',
                    'american-chemical-society',
                    'american-institute-of-physics',
                    'american-society-of-civil-engineers',
            ]
            all_csl = os.listdir(self.csl_p)
            major_csl = [s + '.csl' for s in major_styles if s + '.csl' in all_csl]
            other_csl = [c for c in all_csl if c not in major_csl]
            styles = self.build_styles(major_csl, 'major') + \
                    self.build_styles(other_csl, 'other')
            styles_json = json.dumps(styles, separators=(',', ':'))
            with open (os.path.join(self.p, 'csl_styles.json'), 'wb') as f:
                f.write(styles_json)

    def build_styles(self, csl, category=''):
        xmlns = 'http://purl.org/net/xbiblio/csl'
        output = []
        for c in csl:
            if not c.endswith('.csl'): continue
            tree = ET.parse(os.path.join(self.csl_p, c))
            root = tree.getroot()
            info = root.find('./{%s}info' % xmlns)
            title = info.find('./{%s}title' % xmlns).text
            title_short = info.find('./{%s}title-short' % xmlns)
            if title_short != None:
                title_short = title_short.text
                title += ' (%s)' % title_short
            output.append(OrderedDict([
                    ('id', c.split('.', 1)[0]),
                    ('text', title),
                    ('href', '/ckanext/citation/csl/styles/' + c),
                    ('category', category)])
            )
        return output
