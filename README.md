SIBR STV poll tallier
--------------------

This script exists to tally the preference voting used in [SIBR's team abbreviations survey](https://docs.google.com/forms/d/e/1FAIpQLScvrhej69YBXAG_BwdJTHDhjVP7g_IYOLuT5nkJ9M00UsWzvA/viewform). It uses a variant of Single Transferable Vote that supports people assigning the same preference value to multiple options.

Sample usage
```bash
$ python vote.py  --file abbr.csv --all
$ python vote.py  --file abbr.csv --team Crabs
```

You can set the win threshold using `--threshold`.

In the `--all` case the script will report runners up for cases where the vote is very close.
