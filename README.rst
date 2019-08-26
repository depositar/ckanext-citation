================
ckanext-citation
================

This extension provides a snippet in dataset page
to cite a dataset in a specific citation style.

------------
Requirements
------------

This extension is only tested in CKAN 2.7 and later.

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
