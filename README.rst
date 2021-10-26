================
ckanext-citation
================

This extension provides a snippet in dataset page
to cite a dataset in a specific citation style.

------------
Requirements
------------

This extension is only tested in CKAN 2.9 and later.

------------
Installation
------------

To install ckanext-citation:

1. Activate your CKAN virtual environment, for example::

    . /usr/lib/ckan/default/bin/activate

2. Install the ckanext-citation Python package into your virtual environment::

    pip install 'git+https://github.com/depositar/ckanext-citation.git#egg=ckanext-citation'

3. Add ``citation`` to the ``ckan.plugins`` setting in your CKAN
   config file (by default the config file is located at
   ``/etc/ckan/default/production.ini``).

4. Add a file ``templates/package/read_base.html`` in your custom extension
   (or modify ``/usr/lib/ckan/default/src/ckan/ckan/templates/package/read_base.html`` if
   you are not using a custom extension)::

    {% ckan_extends %}

    {% block secondary_content %}
      {{ super() }}
      {% snippet "citation/package/snippets/citation.html" %}
    {% endblock %}

5. Restart CKAN and Solr. For example if you've deployed CKAN with Apache on Ubuntu::

    sudo service jetty8 restart
    sudo service apache2 reload

-------------
Configuration
-------------

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Mapping between CKAN Fields and `CSL Variables`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Currently only title and author fields are supported. ::

    ckanext.citation.csl_mappings = {"title": "title", "author": "author"}

-----
Usage
-----

^^^^^^^^
Commands
^^^^^^^^

``citation``

1. ``build_styles``: generate a list of citation styles.::

    ckan -c CONFIG citation build_styles

* By default, the following styles will be shown as major styles:

    * apa
    * modern-language-association
    * chicago-note-bibliography
    * chicago-author-date
    * ieee
    * council-of-science-editors
    * american-medical-association
    * american-chemical-society
    * american-institute-of-physics
    * american-society-of-civil-engineers

* You may need to update the citation styles::

    cd /usr/lib/ckan/default/src/ckanext-citation/ckanext/citation/public/ckanext/citation/csl/styles && git pull

.. _`CSL Variables`:  https://docs.citationstyles.org/en/stable/specification.html#appendix-iv-variables
