import numpy as np
import Alphabet


class BeamEntry:
    """Informatia despre un singur beam la un specific time-step"""

    def __init__(self):
        self.prTotal = 0  # probabilitatea pentru blank si non_blank ending sequence
        self.prNonBlank = 0  # prob non-blank
        self.prBlank = 0  # prob blank
        self.prText = 1  # LM
        self.lmApplied = False  # daca LM a fost deja aplicat pentru beamul asta
        self.labeling = ()


class BeamState:
    """Informatii despre beams la un specific time-step"""

    def __init__(self):
        self.entries = {}

    def norm(self):
        """normalizare LM score"""
        for (k, _) in self.entries.items():
            labelingLen = len(self.entries[k].labeling)
            self.entries[k].prText = self.entries[k].prText ** (1.0 / (labelingLen if labelingLen else 1.0))

    def sort(self):
        """returneaza beam-labelings sortate dupa prob"""
        beams = [v for (_, v) in self.entries.items()]
        sortedBeams = sorted(beams, reverse=True, key=lambda x: x.prTotal * x.prText)
        return [x.labeling for x in sortedBeams]


def applyLM(parentBeam, chilBeam, classes, lm):
    """calculam LM scores"""
    if lm and not chilBeam.lmApplied:
        c1 = classes[parentBeam.labeling[-1] if parentBeam.labeling else classes.index(' ')]
        c2 = classes[chilBeam.labeling[-1]]
        lmInfluenta = 0.01
        bigramProb = lm.getCharBigram(c1, c2) ** lmInfluenta  # probabilitatea de a vedea c1 si c2 unul langa altul
        chilBeam.prText = parentBeam.prText * bigramProb
        chilBeam.lmApplied = True


def addBeam(beamstate, labeling):
    """adauga beam daca nu exista"""
    if labeling not in beamstate.entries:
        beamstate.entries[labeling] = BeamEntry()


def ctcBeamSearch(mat, classes, lm, beamWidth=25):
    """beam search la fel ca in articol"""
    # mat = output matrice, classes=alfabetul
    blankIdx = len(classes)  # id-ul caracterului blank
    maxT, maxC = mat.shape

    # init beam state
    last = BeamState()
    labeling = ()
    last.entries[labeling] = BeamEntry()
    last.entries[labeling].prBlank = 1
    last.entries[labeling].prTotal = 1

    # pentru toate time-steps
    for t in range(maxT):
        curr = BeamState()
        # le iau pe cele mai bune in ordine (ultimele beamWidth)
        bestLabelings = last.sort()[0:beamWidth]

        # pentru toate beamurile
        for labeling in bestLabelings:
            # probabilitatea pathurilor terminate in non-blank
            pr_non_blank = 0
            # in cazul in care non-empty beam
            if labeling:  # probabilitatea cu dublare a ultimei litere
                pr_non_blank = last.entries[labeling].prNonBlank * mat[
                    t, labeling[-1]]  # la fel ca mat[t][..] dar e mai rapid
            pr_blank = last.entries[labeling].prTotal * mat[t, blankIdx]

            # addaugam beam la acest time-step
            addBeam(curr, labeling)
            # adaug data
            curr.entries[labeling].labeling = labeling
            curr.entries[labeling].prNonBlank += pr_non_blank
            curr.entries[labeling].prBlank += pr_blank
            curr.entries[labeling].prTotal += pr_blank + pr_non_blank
            curr.entries[labeling].prText = last.entries[labeling].prText  # beam-labeling not changed
            curr.entries[labeling].lmApplied = True

            # extindere
            for c in range(maxC - 1):
                new_labeling = labeling + (c,)
                # daca se termina cu duplicare la final, consideram doar pe cele care se termina cu blank
                if labeling and labeling[-1] == c:
                    pr_non_blank = mat[t, c] * last.entries[labeling].prBlank
                else:
                    pr_non_blank = mat[t, c] * last.entries[labeling].prTotal

                # daca nu mai exista il aduagam
                addBeam(curr, new_labeling)

                curr.entries[new_labeling].labeling = new_labeling
                curr.entries[new_labeling].prNonBlank += pr_non_blank
                curr.entries[new_labeling].prTotal += pr_non_blank

                applyLM(curr.entries[labeling], curr.entries[new_labeling], classes, lm)
        last = curr

    last.norm()
    best_labeling = last.sort()[0]
    # decodare
    # todo: after testing move to Alphabet.label_to_text
    res = ''
    for l in best_labeling:
        res += classes[l]

    return res


def create_npy(text, alphabet):
    mat = np.zeros((32, 80))
    t = 0
    for c in text:
        mat[t, alphabet.find(c)] = 1
        t += 1

    return mat


def test_beam_search():
    """test decoder"""
    classes = ' !”#&’()*+,-./0123456789:;?ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    mat = create_npy('buna', classes)
    print(mat)
    print('Test beam search')
    expected = 'a'
    actual = ctcBeamSearch(mat, classes, None)
    print('Expected: ' + expected)
    print('Actual: ' + actual)
    print('OK' if expected == actual else 'ERROR')
