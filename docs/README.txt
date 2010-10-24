inigo.tracxmlrpc
****************************

Introduction
============



How to use?
===========

You can import inigo.tracxmlrpc from ``inigo.tracxmlrpc`` and ``.need`` it
where you want these resources to be included on a page::

  from inigo.tracxmlrpc import tracxmlrpc

  .. in your page or widget rendering code, somewhere ..

  tracxmlrpc.need()

This requires integration between your web framework and
``hurry.resource``, and making sure that the original resources
(shipped in the ``tracxmlrpc-build`` directory in ``inigo.tracxmlrpc``)
are published to some URL.

The package has already been integrated for Grok_ and the Zope
Toolkit. If you depend on the `hurry.zoperesource`_ package in your
``setup.py``, the above example should work out of the box. Make sure
to depend on the `hurry.zoperesource`_ package in your ``setup.py``.

.. _`hurry.zoperesource`: http://pypi.python.org/pypi/hurry.zoperesource

.. _Grok: http://grok.zope.org

Preparing inigo.tracxmlrpc before release
====================================================

This section is only relevant to release managers of ``inigo.tracxmlrpc``.

When releasing ``inigo.tracxmlrpc``, an extra step should be
taken. Follow the regular package `release instructions`_, but before
egg generation (``python setup.py register sdist upload``) first
execute ``bin/tracxmlrpcprepare <version number>``, where version number
is the version of the release, such as ``1.0.1``. This will
download the inigo.tracxmlrpc library of that version and place it in the
egg.

.. _`release instructions`: http://grok.zope.org/documentation/how-to/releasing-software
