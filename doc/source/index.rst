.. fooNelnet documentation master file, created by
   sphinx-quickstart on Wed Oct 29 12:57:59 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

fooNelnet
=====================================

A better autopayment system for Nelnet users.

fooNelnet is a web bot that can automatically record loan status data from Nelnet and save it in a google spreadsheet. It can also automatically initiate payments.

I built fooNelnet because I wanted to keep better track of my student loans, and I found the process of getting loan status data from Nelnet into a spreadsheet rather painful to do manually. Once I had the platform built I realized that I could also use to make automated payments. I determined that since student loans accrue interest at a daily rate, if you make daily payments you save on interest over the life of the loan. So I added a feature that enables fooNelnet to make small daily loan payments instead of a single large monthly one.

Be aware that fooNelnet will take tell Nelnet to initiate money transfers out of you bank account. There are no sanity checks, so if set up improperly it could empty or overdraw on your account.

.. note:: fooNelnet is named after the classic programming term "foo." The fact that you could phonetically respell it as FU-Nelnet is entirly coincidental.

Usage:
    ./fooNelnet.py [-record_data] [-make_payment]

Contents:

.. toctree::
   :maxdepth: 2
   
   fooNelnet



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

