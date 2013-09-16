# author   : Johann-Mattis List
# email    : mattis.list@uni-marburg.de
# created  : 2013-09-05 18:22
# modified : 2013-09-05 18:22
"""
Module provides methods for the evaluation of automatic linguistic reconstruction analyses.
"""

__author__="Johann-Mattis List"
__date__="2013-09-05"

from ..settings import rcParams,rc
from ..align.pairwise import edit_dist
from ..sequence.sound_classes import ipa2tokens,tokens2class

def mean_edit_distance(
        wordlist,
        gold = "proto",
        test = "consensus",
        ref = "cogid",
        tokens = True,
        classes = False,
        **keywords
        ):
    """
    Function computes the edit distance between gold standard and test set.

    Parameters
    ----------
    wordlist : ~lingpy.basic.wordlist.Wordlist
        The wordlist object containing the data for a given analysis.
    gold : str (default="proto")
        The name of the column containing the gold-standard solutions.
    test = "consensus"
        The name of the column containing the test solutions.
    
    Returns
    -------
    dist : float
        The mean edit distance between gold and test reconstructions.
    """
    defaults = dict(
            merge_vowels = rcParams['merge_vowels'],
            model = rcParams['model']
            )
    for k in defaults:
        if k not in keywords:
            keywords[k] = defaults[k]
    
    distances = []
    etd = wordlist.get_etymdict(ref=ref)
    
    for key,idxs in etd.items():
        
        # get only valid numbers for index-search
        idx = [idx[0] for idx in idxs if idx != 0][0]

        if rcParams['debug']: print(idx,idxs)
        
        # get proto and consensus from wordlist
        proto = wordlist[idx,gold]
        consensus = wordlist[idx,test]

        if rcParams['debug']: print(proto,consensus)
    
        
        if tokens or classes:
            proto = ipa2tokens(proto,**keywords)
            consensus = ipa2tokens(consensus,**keywords)

            if classes:
                proto = tokens2class(proto,**keywords)
                consensus = tokens2class(consensus,**keywords)
        
        d = edit_dist(
                proto,
                consensus,
                normalized = False
                )
        distances += [d]

    med = sum(distances) / len(distances)

    if rcParams['verbose']: print("MEAN ED: {0:.2f}".format(med))

    return med

def med(
        wordlist,
        gold = "proto",
        test = "consensus",
        ref = "cogid",
        tokens = True,
        classes = False,
        **keywords
        ):
    # alias for mean_edit_distance
    return mean_edit_distance(wordlist,gold,test,ref,tokens,classes,**keywords)
