substitution-solver
=========

#####Solves simple substitution ciphers by matching word patterns with a dictionary.

usage: python subsolve.py wordlist-file ciphertext-file

A good wordlist is important for best results. Ideally a wordlist should include every word that could appear in the plaintext, without including too many extraneous words. In particular, I recommend removing uncommon 1, 2, and 3 letter words.  

This software, except for the included wordlist.txt, is in the public domain.

The included wordlist is from SCOWL (http://wordlist.aspell.net/). Below is SCOWL's copyright notice:

```
Copyright 2000-2015 by Kevin Atkinson

Permission to use, copy, modify, distribute and sell these word
lists, the associated scripts, the output created from the scripts,
and its documentation for any purpose is hereby granted without fee,
provided that the above copyright notice appears in all copies and
that both that copyright notice and this permission notice appear in
supporting documentation. Kevin Atkinson makes no representations
about the suitability of this array for any purpose. It is provided
"as is" without express or implied warranty.
```
