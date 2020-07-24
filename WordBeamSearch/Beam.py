from __future__ import division
from __future__ import print_function

import copy  # ca sa putem copia si atunci cand modificam sa nu se modif si ob initial


class Optical:
    """scorul pentru beam"""

    def __init__(self, pr_blank=0.0, pr_non_blank=0.0):
        self.prBlank = pr_blank  # probabilitatea ca sa se termine in blank
        self.prNonBlank = pr_non_blank  # probabilitatea ca sa se termine in non-blank


class Textual:
    """scorul textual pentru bea,"""
    def __init__(self, text=''):
        self.text = text
        self.wordHist = []  # istoricul cuvintelor
        self.wordDev = []  # cuvinte in formare
        self.prUnnormalized = 1.0
        self.prTotal = 1.0


class Beam:
    """beamul cu textul si scorul respectiv"""

    def __init__(self, lm, use_n_grams):
        """
        creaza un beam
        :param lm: language model
        :param use_n_grams:
        """
        self.optical = Optical(1.0, 0.0)
        self.textual = Textual('')
        self.lm = lm
        self.useNGrams = use_n_grams

    def merge_beam(self, beam):
        """merge a doua beamuri cu acelasi text - ad probab ( ex -a aa a- reprezinta a)"""
        if self.get_text() != beam.get_text():
            raise Exception('mergeBeam: texte differite')

        self.optical.prNonBlank += beam.get_pr_nonblank()
        self.optical.prBlank += beam.get_pr_blank()

    def get_text(self):
        return self.textual.text

    def get_pr_blank(self):
        return self.optical.prBlank

    def get_pr_nonblank(self):
        return self.optical.prNonBlank

    def get_pr_total(self):
        return self.get_pr_blank() + self.get_pr_nonblank()

    def get_pr_textual(self):
        return self.textual.prTotal

    def get_next_chars(self):
        return self.lm.get_next_chars(self.textual.wordDev)

    def create_child_beam(self, newChar, prBlank, prNonBlank):
        """
        extindem beam cu caracter nou + calc scor
        :param newChar: caracterul care se adauga beamului curent
        :param prBlank: probabil ca sa se termine in blank
        :param prNonBlank: probab ca sa se termine in non-blank
        :return: returneaza beamul
        """
        beam = Beam(self.lm, self.useNGrams)

        # copiem informatia text
        beam.textual = copy.deepcopy(self.textual)
        beam.textual.text += newChar

        # calculam doar daca se extinde
        if newChar != '':
            if self.useNGrams:
                """util unigrams si bigrams"""
                # todo: uneste cu unigrams si bigrams
                print('not implemented yet')
            else:
                if newChar in beam.lm.get_word_chars():
                    beam.textual.wordDev += newChar
                else:
                    beam.textual.wordDev = ''

        beam.optical.prBlank = prBlank
        beam.optical.prNonBlank = prNonBlank
        return beam

    def __str__(self):
        return '"' + self.get_text() + '"' + ';' + str(self.get_pr_total()) + ';' + str(self.get_pr_textual()) + ';' + \
               str(self.textual.prUnnormalized)


class BeamList:
    """lista beamurilor la un specific timestep"""

    def __init__(self):
        self.beams = {}

    def add_beam(self, beam):
        """add or merge beam into list"""
        # daca nu a mai fost vazut
        if beam.get_text() not in self.beams:
            self.beams[beam.get_text()] = beam
        else:
            self.beams[beam.get_text()].merge_beam(beam)

    def get_best_beams(self, num):
        """
        cele mai bune beamuri
        :param num: beam-width (cate cele mai bune beamuri sa le tinem)
        :return: cele mai bune beamuri
        """
        u = [v for (_, v) in self.beams.items()]
        lm_weight = 1
        return sorted(u, reverse=True, key=lambda x: x.get_pr_total() * (x.get_pr_textual() ** lm_weight))[:num]

    def delete_partial_beam(self, lm):
        """stergem beamurile cu cuvant neterminat"""
        for (k, v) in self.beams.items():
            last_words = v.textual.wordDev
            if last_words != '' and not lm.is_word(last_words):
                del self.beams[k]

    def complete_beams(self, lm):
        """beamuri complete - ultimul cuv complet"""
        for (_, v) in self.beams.items():
            last_prefix = v.textual.wordDev
            if last_prefix == '' or lm.is_word(last_prefix):
                continue

            # luam candidatul cu prefixul asta
            words = lm.get_next_words(last_prefix)
            # if there is just one candidate, then the last prefix can be extended to
            if len(words) == 1:
                word = words[0]
                v.textual.text += word[len(last_prefix) - len(word):]
