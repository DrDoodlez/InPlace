import controller_tests, model_tests
import unittest

modelSuite = model_tests.suite
controllerSuite = controller_tests.suite

all_tests = unittest.TestSuite([modelSuite, controllerSuite])
