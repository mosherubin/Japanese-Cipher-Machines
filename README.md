======
Japanese Cipher Machines (1930-1945)
======

Simulations of Japanese cipher machines from 1930-1945
------------------------------------------------------

:Author: Moshe Rubin <moshe.rubin@gmail.com>
:Version: 0.1
:Date: December 25, 2021
:Home Page: 
:License: MIT License (see LICENSE.txt)
:Documentation: This file
:Support: 

This project is a Python library and command-line utility for simulating the
Japanese IKA Machine, ...

This project is a Python 3 library and command-line utility for encrypting and
decrypting text by simulating the operation of an actual PURPLE machine.

If you are brand new to the ``IKA`` cipher machine, please skip down to the
references section and familiarize yourself with the device. This will help you
understand the terminology used in the documentation, below.


Requirements
############

``Purple`` was written in Python_ 3, specifically 3.3.2, and has no other external
dependencies.


Installation
############

To run the unit tests::

   $ cd where-you-extracted-purple
   $ python -m unittest discover


Initial Settings Syntax
#######################



Command-line Usage
##################

To get help on the command-line ``Purple`` utility, execute the ``purple``
command with the ``--help`` option::

   $ purple --help
   usage: purple [-h] [-e] [-d] [-f] [-s SWITCHES] [-a ALPHABET] [-t TEXT]
                 [-i FILE] [-g N] [-w N]

   PURPLE cipher machine simulator

   optional arguments:
     -h, --help            show this help message and exit
     -e, --encrypt         perform an encrypt operation
     -d, --decrypt         perform a decrypt operation
     -f, --filter          filter plaintext and provide useful substitutions
     -s SWITCHES, --switches SWITCHES
                           switch settings, e.g. 9-1,24,6-23
     -a ALPHABET, --alphabet ALPHABET
                           plugboard wiring string, 26-letters; e.g.
                           AEIOUYBCDFGHJKLMNPQRSTVWXZ
     -t TEXT, --text TEXT  input text to encrypt/decrypt
     -i FILE, --input FILE
                           file to read input text from, - for stdin
     -g N, --group N       if non-zero, group output in N-letter groups [default:
                           5]
     -w N, --width N       wrap output text to N letters; a value of 0 means do
                           not wrap [default: 70]

   Supply either -e or -d, but not both, to perform either an encrypt or decrypt.
   If the -s option is not supplied, the value of the environment variable
   PURPLE97_SWITCHES will be used. If the -a option is not supplied, the value of
   the environment variable PURPLE97_ALPHABET will be used. Input text is
   supplied either by the -t or by the -f options, but not both.

The ``purple`` command operates in two modes, either encrypt (specified with
``-e`` or ``--encrypt``) or decrypt (``-d`` or ``--decrypt``). Input text can
be specified on the command-line with the ``-t`` or ``--text`` option, or
a read from a file (``-i`` or ``--input``).


Library Usage
#############

To use ``Purple`` from within Python code you must first construct
a ``Purple97`` object, which represents a single PURPLE cipher machine. The
constructor is given below::

   class Purple97(switches_pos=None, fast_switch=1, middle_switch=2,
                  alphabet=None)


Support
#######

To report a bug or suggest a feature, please use the issue tracker at the
`Purple Bitbucket page`_. You can also email the author using the address at
the top of this file.


References
##########

#. *PURPLE Revealed: Simulation and Computer-aided Cryptanalysis of Angooki
   Taipu B*, by Wes Freeman, Geoff Sullivan, and Frode Weierud. This paper
   was published in Cryptologia, Volume 27, Issue 1, January, 2003, pp. 1-43.
#. Frode Weierud's CryptoCellar page: `The PURPLE Machine`_
#. Wikipedia Article: `PURPLE Machine`_

The paper in reference 1 is also available here:
http://cryptocellar.web.cern.ch/cryptocellar/pubs/PurpleRevealed.pdf

This simulator would not have been possible without Frode Weierud's
CryptoCellar page and the detailed explanations and analysis found in reference
1. The author is also deeply grateful for email discussions with Frode Weierud
and Geoff Sullivan who provided me with plaintext, advice, and encouragement.

The ``Purple`` simulator's operation was checked against the simulator found in
reference 2.


.. _PURPLE Machine: http://en.wikipedia.org/wiki/Purple_(cipher_machine)
.. _Python: http://www.python.org
.. _Python Package Index: http://pypi.python.org/pypi/purple/
.. _virtualenv: http://www.virtualenv.org/
.. _pip: http://www.pip-installer.org
.. _Purple Bitbucket page: https://bitbucket.org/bgneal/purple/
.. _Mercurial: http://mercurial.selenic.com/
.. _The PURPLE Machine: http://cryptocellar.web.cern.ch/cryptocellar/simula/purple/
