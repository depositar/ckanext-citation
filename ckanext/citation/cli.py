import os
import click
import inspect
import xml.etree.cElementTree as ET

from ckan.common import json

m = __import__('ckanext.citation', fromlist=[''])
p = os.path.join(
        os.path.dirname(inspect.getfile(m)),
        'public', 'ckanext', 'citation', 'csl')
csl_p = os.path.join(p, 'styles')
csl_cp = os.path.join(p, 'custom_styles')


@click.group(u'citation')
def citation():
    '''Citation commands'''
    pass

@citation.command(u'build_styles')
def build_style_cmd():
    '''Generates a list of citation styles.
    By default, the following styles will be shown first:
    apa, modern-language-association, chicago-note-bibliography,
    chicago-author-date, and ieee.
    '''
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
    all_csl = os.listdir(csl_p)
    major_csl = [s + '.csl' for s in major_styles if s + '.csl' in all_csl]
    other_csl = [c for c in all_csl if c not in major_csl]
    styles = build_styles(major_csl, 'major') + \
            build_styles(other_csl, 'other')
    styles_json = json.dumps(styles, separators=(',', ':'))
    with open (os.path.join(p, 'csl_styles.json'), 'w') as f:
        f.write(styles_json)

def build_styles(csl, category=''):
    xmlns = 'http://purl.org/net/xbiblio/csl'
    output = []
    for c in csl:
        href = '/ckanext/citation/csl/styles/'
        if not c.endswith('.csl'): continue
        tree = ET.parse(os.path.join(csl_p, c))
        root = tree.getroot()
        info = root.find('./{%s}info' % xmlns)
        title = info.find('./{%s}title' % xmlns).text
        title_short = info.find('./{%s}title-short' % xmlns)
        if title_short != None:
            title_short = title_short.text
            title += ' (%s)' % title_short
        if os.path.exists(os.path.join(csl_cp, c)):
            # Use custom CSL styles if exist
            href = '/ckanext/citation/csl/custom_styles/'
        output.append(dict([
                ('id', c.split('.', 1)[0]),
                ('text', title),
                ('href', href + c),
                ('category', category)])
        )
    return output

def get_commands():
    return [citation]
