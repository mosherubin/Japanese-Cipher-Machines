# Japanese Cipher Machines (1930-1945)

## Simulations of Japanese cipher machines from 1930-1945

|   |  |
| ------------- | ------------- |
| Author | Moshe Rubin <moshe.rubin@gmail.com> |
| Version | 0.1 |
| Date | December 19, 2021 |
| License | MIT License (see LICENSE.txt) |
| Documentation | This file |

This project is a Python 3 library for simulating several Japanese cipher 
machines used by the Japanese military and diplomatic corps between the years
1930-1945.  The library includes reusable cryptographic components used to 
implement the aforementioned cipher machines.

If you are new to the Japanese cipher machines listed in this documentation, 
please skip down to the references section and familiarize yourself with the devices. 
This will help you understand the terminology used in the documentation.

## Requirements

The Japanese cipher machines and components in this library were was written in Python 3, starting with version 3.7.0, and has no other external
dependencies.

## Installation



## Initial Settings Syntax



## Command-line Usage

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


## Library Usage

To use ``Purple`` from within Python code you must first construct
a ``Purple97`` object, which represents a single PURPLE cipher machine. The
constructor is given below::

   class Purple97(switches_pos=None, fast_switch=1, middle_switch=2,
                  alphabet=None)


## Support

To report a bug or suggest a feature, please use the issue tracker at the
`Purple Bitbucket page`_. You can also email the author using the address at
the top of this file.


## References

1. *The Imperial Japanese Navy IKA Cipher Machine*, by Chris Christensen.  This paper was published in the Proceedings of the 4th International Conference on Historical Cryptology, HistoCrypt 2021, pp. 38-47 ([downloadable here](https://ecp.ep.liu.se/index.php/histocrypt/article/view/155), last accessed 19 December 2021). 
2. *Big Machines: Cryptographic Security of the German Enigma, Japanese PURPLE, and US SIGABA/ECM Cipher machines* (2018), by Stephen J. Kelley, pp. 43-50.
3. *Development of the First Japanese Cipher Machine: RED*, by Satoshi Tomokiyo, http://cryptiana.web.fc2.com/code/redciphermachine.htm (last accessed: 19 December 2021).
4. *Pearl Harbor and the Inadequacy of Cryptanalysis*, David Kahn, Cryptologia Vol. 15 No. 4 (1991), pp. 273-294.
