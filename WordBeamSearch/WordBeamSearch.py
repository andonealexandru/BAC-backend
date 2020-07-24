from __future__ import division
from __future__ import print_function

import numpy as np

from Beam import Beam, BeamList
from LanguageModel import LanguageModel


def wordBeamSearch(mat, beamWidth, lm, useNgrams):
    """
    :param mat: outputul de la rnn TxC
    :param beamWidth: de cate cele mai bune beamuri sa tina cont (dp[i] = max(dp[i-1], ..., dp[i-bw])
    :param lm: language model
    :param useNgrams: Ngrams
    :return:
    """
    chars = lm.get_all_chars()
    blank_idx = len(chars)
    maxt, _ = mat.shape

    genesis_beam = Beam(lm, useNgrams)  # string gol
    last = BeamList()  # lista cu beamuri la un time step
    last.add_beam(genesis_beam)

    # pt fiecare time step
    for t in range(maxt):
        curr = BeamList()  # lista beamurilor la stepul curent

        best_beams = last.get_best_beams(beamWidth)
        for beam in best_beams:
            # probab ca sa se termine in non-blank
            pr_non_blank = 0
            if beam.get_text() != '':
                # charul la timestepul current trb sa fie cel anterior
                label_idx = chars.index(beam.get_text()[-1])
                pr_non_blank = beam.get_pr_nonblank() * mat[t, label_idx]

            # probab sa se termine cu blank
            pr_blank = beam.get_pr_total() * mat[t, blank_idx]

            # salvam
            curr.add_beam(beam.create_child_beam('', pr_blank, pr_non_blank))  #extinzand cu un car identic sau cu blank
                    # , textul nu se schimba ('')

            nextChars = beam.get_next_chars()
            for c in nextChars:
                # extindem cu caracter diferit
                label_idx = chars.index(c)
                if beam.get_text() != '' and beam.get_text()[-1] == c:
                    pr_non_blank = mat[t, label_idx] * beam.get_pr_blank()  # caractere separate de blank
                else:
                    pr_non_blank = mat[t, label_idx] * beam.get_pr_total()

                # salvam
                curr.add_beam(beam.create_child_beam(c, 0, pr_non_blank))
        last = curr
    last.complete_beams(lm)
    best_beams = last.get_best_beams(1)  #probabilitatea
    return best_beams[0].get_text()

#  t1   t2
#a 0.3  0.3
#b 0.1  0.1
#  0    0
#- 0.6  0.6

# test
testLM = LanguageModel('a b aa ab ba bb', 'ab ', 'ab')
testMat = np.array([[0.3, 0.1, 0, 0.6], [0.3, 0.1, 0, 0.6]])
testBW = 25
res = wordBeamSearch(testMat, testBW, testLM, False)
print('Result: ' + res)
