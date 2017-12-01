# -*- coding: utf-8 -*-
"""
Created on Tue Jun 28 13:18:34 2016

@author: okada
"""

import unittest
import os
import sys
import test_utils
import subprocess

class TestSet(unittest.TestCase):

    CURRENT = os.path.dirname(__file__)
    dataset = CURRENT + "/dataset/"
    REF = CURRENT + "/ref/"
    ALT = CURRENT + "/src/"
    
    # init class
    @classmethod
    def setUpClass(cls):
        import shutil
        if os.path.exists(cls.ALT):
            shutil.rmtree(cls.ALT)
        os.makedirs(cls.ALT)
        
    # terminated class
    @classmethod
    def tearDownClass(cls):
        pass

    # init method
    def setUp(self):
        pass

    # terminated method
    def tearDown(self):
        pass
        
    def test1_01_qc(self):
        subprocess.check_call('python paplot qc %s/qc/cover/merge.csv %s html -c %s/qc/cover/paplot.cfg' % (self.dataset, self.ALT, self.dataset), shell=True)
        
        ref = test_utils.load_text(self.REF + "qc/test1_01_sample_header_id_csv/data_qc.js")
        alt = test_utils.load_text(self.ALT + "html/data_qc.js")
        self.assertEqual(ref, alt)

        ref = test_utils.load_html(self.REF + "qc/test1_01_sample_header_id_csv/graph_qc.html")
        alt = test_utils.load_html(self.ALT + "html/graph_qc.html")
        self.assertEqual(ref, alt)
        
    def test1_02_ca(self):
        subprocess.check_call('python paplot ca %s/ca/cover/merge.csv %s html -c %s/ca/cover/paplot.cfg' % (self.dataset, self.ALT, self.dataset), shell=True)

        ref = test_utils.load_text(self.REF + "ca/test1_01_sample_header_id_csv/data_ca.js")
        alt = test_utils.load_text(self.ALT + "html/data_ca.js")
        self.assertEqual(ref, alt)
        
        ref = test_utils.load_html(self.REF + "ca/test1_01_sample_header_id_csv/graph_ca.html")
        alt = test_utils.load_html(self.ALT + "html/graph_ca.html")
        self.assertEqual(ref, alt)

    def test1_03_mutation(self):
        subprocess.check_call('python paplot mutation %s/mutation/cover/merge.csv %s html -c %s/mutation/cover/paplot.cfg' % (self.dataset, self.ALT, self.dataset), shell=True)

        ref = test_utils.load_text(self.REF + "mutation/test2_01_sample_header_id_csv_summary/data_mutation.js")
        alt = test_utils.load_text(self.ALT + "html/data_mutation.js")
        self.assertEqual(ref, alt)
        
        ref = test_utils.load_html(self.REF + "mutation/test2_01_sample_header_id_csv_summary/graph_mutation.html")
        alt = test_utils.load_html(self.ALT + "html/graph_mutation.html")
        self.assertEqual(ref, alt)

    def test1_04_signature(self):
        subprocess.check_call('python paplot signature %s/signature/cover/data2.json %s html -c %s/signature/cover/paplot.cfg' % (self.dataset, self.ALT, self.dataset), shell=True)

        ref = test_utils.load_text(self.REF + "signature/test1_02_stack/data_signature2.js")
        alt = test_utils.load_text(self.ALT + "html/data_signature2.js")
        self.assertEqual(ref, alt)

        ref = test_utils.load_html(self.REF + "signature/test1_02_stack/graph_signature2.html")
        alt = test_utils.load_html(self.ALT + "html/graph_signature2.html")
        self.assertEqual(ref, alt)
        
    def test1_05_pmsignature(self):
        subprocess.check_call('python paplot pmsignature %s/pmsignature/cover/data2.json %s html -c %s/pmsignature/cover/paplot.cfg' % (self.dataset, self.ALT, self.dataset), shell=True)

        ref = test_utils.load_text(self.REF + "pmsignature/test1_02_stack/data_pmsignature2.js")
        alt = test_utils.load_text(self.ALT + "html/data_pmsignature2.js")
        self.assertEqual(ref, alt)

        ref = test_utils.load_html(self.REF + "pmsignature/test1_02_stack/graph_pmsignature2.html")
        alt = test_utils.load_html(self.ALT + "html/graph_pmsignature2.html")
        self.assertEqual(ref, alt)
