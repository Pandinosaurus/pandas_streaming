#-*- coding: utf-8 -*-
"""
@brief      test log(time=20s)
"""

import sys
import os
import unittest
from collections import Counter
import pandas


try:
    import pyquickhelper as skip_
except ImportError:
    path = os.path.normpath(
        os.path.abspath(
            os.path.join(
                os.path.split(__file__)[0],
                "..",
                "..",
                "..",
                "pyquickhelper",
                "src")))
    if path not in sys.path:
        sys.path.append(path)
    import pyquickhelper as skip_


try:
    import src
except ImportError:
    path = os.path.normpath(
        os.path.abspath(
            os.path.join(
                os.path.split(__file__)[0],
                "..",
                "..")))
    if path not in sys.path:
        sys.path.append(path)
    import src

from pyquickhelper.loghelper import fLOG
from pyquickhelper.pycode import ExtTestCase
from src.pandas_streaming.df import train_test_connex_split


class TestConnexSplitBig(ExtTestCase):

    def _test_conex_big(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        data = os.path.join(os.path.dirname(__file__), "data")
        name = os.path.join(data, "buggy_hash.csv")
        df = pandas.read_csv(name, sep="\t", encoding="utf-8")
        train, test, stats = train_test_connex_split(df, fLOG=fLOG,
                                                     groups=[
                                                         "cart_id", "mail", "product_id"],
                                                     fail_imbalanced=0.9, return_cnx=True)
        self.assertGreater(train.shape[0], 0)
        self.assertGreater(test.shape[0], 0)
        elements = stats[1]['connex']
        counts = Counter(elements)
        nbc = len(counts)
        maxi = max(counts.values())
        self.assertEqual(nbc, 5376)
        self.assertEqual(maxi, 14181)

    def test_conex_big_approx(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        data = os.path.join(os.path.dirname(__file__), "data")
        name = os.path.join(data, "buggy_hash.csv")
        df = pandas.read_csv(name, sep="\t", encoding="utf-8")
        train, test, stats = train_test_connex_split(df, fLOG=fLOG,
                                                     groups=[
                                                         "cart_id", "mail", "product_id"],
                                                     stop_if_bigger=0.05, return_cnx=True,
                                                     keep_balance=0.8)
        self.assertGreater(train.shape[0], 0)
        self.assertGreater(test.shape[0], 0)
        elements = stats[1]['connex']
        counts = Counter(elements)
        nbc = len(counts)
        maxi = max(counts.values())
        self.assertGreater(nbc, 5376)
        self.assertLesser(maxi, 14181)


if __name__ == "__main__":
    unittest.main()
