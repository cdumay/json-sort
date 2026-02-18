*********
json-sort
*********

Just a tiny tool to sort keys in a json file

----------
Quickstart
----------

First, install json-sort using
`pip <https://pip.pypa.io/en/stable/>`_::

    sh-4.2$ pip install json-sort

Next, use :code:`json-sort-fromfile` or :code:`json-sort-fromremote`::

    sh-4.2$ json-sort-fromremote http://headers.jsontest.com/
    {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Host": "headers.jsontest.com",
        "User-Agent": "python-requests/2.10.0",
        "X-Cloud-Trace-Context": "8de3c28b6c503d26d38c1c7d6111bfa6/11298559371430510765"
    }

---------
Arguments
---------

To see binaries usage, just set :code:`-h`::

    usage: json-sort-fromfile [-h] [--output FILE] [--verbose] file

    positional arguments:
      file                  input file

    optional arguments:
      -h, --help            show this help message and exit
      --output FILE, -o FILE
                            output file (default: stdout)
      --verbose             increase output verbosity

Example::

    sh-4.2$ json-sort-fromfile --verbose --output test2.json ../test.json
    DEBUG   : Checking file: /tmp/test.json
    DEBUG   : Saving to: /tmp/json-sort/test2.json

--------
Testing
--------

Install dev dependencies and run tests (coverage ≥ 90%)::

    pip install -r requirements-dev.txt
    PYTHONPATH=src pytest tests/ -v
    PYTHONPATH=src python -m coverage run --source=src/json_sort -m pytest tests/ -q
    PYTHONPATH=src python -m coverage report --fail-under=90

-------
License
-------

Apache License 2.0