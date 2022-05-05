from ..core_functions.bootstrap import runIndependentBootstrap, runJointBootstrap
from ..ICHelpers import completeICFromInputs
import unittest
import numpy as np
import numpy.testing as nptest
from pathlib import Path
from .tests_IC import fwdIC, bckwdIC, nSamples, yfitIC
testPath = Path(__file__).absolute().parent 

np.random.seed(1)   # Set seed so that tests match everytime

fwdICDefault = fwdIC
bckwdICDefault = bckwdIC
yfitICDefault = yfitIC

#TODO: Figure out why doing the two tests simultaneously fails the testing

# Test Joint procedure
bootJointResults = runJointBootstrap(bckwdICDefault, fwdICDefault, nSamples, yfitICDefault, checkUserIn=False)

bootSamples = []
for bootRes in bootJointResults:
    bootSamples.append(bootRes.bootSamples)

bootBackSamples, bootFrontSamples, bootYFitSamples = bootSamples

oriBootBack = testPath / "stored_boot_back.npz"
oriBootFront = testPath / "stored_boot_front.npz"
oriBootYFit = testPath / "stored_boot_yfit.npz"

class TestJointBootstrap(unittest.TestCase):

    def setUp(self):
        self.oriJointBack = np.load(oriBootBack)["boot_samples"]
        self.oriJointFront = np.load(oriBootFront)["boot_samples"]
        self.oriJointYFit = np.load(oriBootYFit)["boot_vals"]

    def testBack(self):
        nptest.assert_array_almost_equal(bootBackSamples, self.oriJointBack)

    def testFront(self):
        nptest.assert_array_almost_equal(bootFrontSamples, self.oriJointFront)

    def testYFit(self):
        nptest.assert_array_almost_equal(bootYFitSamples, self.oriJointYFit)


# # Test Single procedure
# bootSingleResults = runIndependentBootstrap(bckwdIC, nSamples, yfitIC, checkUserIn=False)

# bootSingleBackSamples = bootSingleResults[0].bootSamples
# bootSingleYFitSamples = bootSingleResults[1].bootSamples

# oriSingleBootBack = testPath / "stored_single_boot_back.npz"
# oriSingleBootYFit = testPath / "stored_single_boot_back_yfit.npz"

# class TestIndependentBootstrap(unittest.TestCase):
#     def setUp(self):
#         self.oriBack = np.load(oriSingleBootBack)["boot_samples"]
#         self.oriYFit = np.load(oriSingleBootYFit)["boot_vals"]

#     def testBack(self):
#         nptest.assert_array_almost_equal(bootSingleBackSamples, self.oriBack)

#     def testYFit(self):
#         nptest.assert_array_almost_equal(bootSingleYFitSamples, self.oriYFit)

