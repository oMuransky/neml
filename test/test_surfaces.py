import sys
sys.path.append('..')

from neml.surfaces import *
from common import *

import unittest
import numpy as np
import numpy.linalg as la

class CommonYieldSurface(object):
  """
    Inherit from me and define setUp to run standard tests over a yield
    surface.
  """
  def test_dfds(self):
    dfn = lambda s: self.model.f(s, self.hist, self.T)
    n_d = differentiate(dfn, self.s)
    self.assertTrue(np.allclose(n_d, 
      self.model.df_ds(self.s, self.hist, self.T)))

  def test_dfdq(self):
    dfn = lambda q: self.model.f(self.s, q, self.T)
    n_d = differentiate(dfn, self.hist)
    self.assertTrue(np.allclose(n_d, 
      self.model.df_dq(self.s, self.hist, self.T)))

  def test_dfdsds(self):
    dfn = lambda s: self.model.df_ds(s, self.hist, self.T)
    n_d = differentiate(dfn, self.s)
    self.assertTrue(np.allclose(n_d,
      self.model.df_dsds(self.s, self.hist, self.T)))
    
  def test_dfdqdq(self):
    dfn = lambda q: self.model.df_dq(self.s, q, self.T)
    n_d = differentiate(dfn, self.hist)
    self.assertTrue(np.allclose(n_d,
      self.model.df_dqdq(self.s, self.hist, self.T)))

  def test_dfdsdq(self):
    dfn = lambda q: self.model.df_ds(self.s, q, self.T)
    n_d = differentiate(dfn, self.hist)
    self.assertTrue(np.allclose(n_d,
      self.model.df_dsdq(self.s, self.hist, self.T)))

  def test_dfdqds(self):
    dfn = lambda s: self.model.df_dq(s, self.hist, self.T)
    n_d = differentiate(dfn, self.s)
    self.assertTrue(np.allclose(n_d,
      self.model.df_dqds(self.s, self.hist, self.T)))

class TestIsoJ2(unittest.TestCase, CommonYieldSurface):
  def setUp(self):
    self.s = np.array([10.0,-50.0,250.0,25.0,33.0,-40.0])
    self.hist = np.array([-150.0])
    self.T = 300.0

    self.model = IsoJ2()

  def test_hist(self):
    self.assertEqual(self.model.nhist, 1)

  def test_f(self):
    sdev = self.s - np.array([1,1,1,0,0,0]) * np.sum(self.s[:3])/3
    exact = la.norm(sdev) + np.sqrt(2.0/3.0) * self.hist[0]
    self.assertTrue(np.isclose(self.model.f(self.s, self.hist, self.T),
      exact), 
      msg = str(self.model.f(self.s, self.hist, self.T)))
