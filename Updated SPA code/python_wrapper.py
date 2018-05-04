from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
# import matlab.engine
import spa_python
import numpy as np
import os

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)


class Error(Exception):
    """
    Generic custom exception written mostly to be extended by other
    exceptions.
    """
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return "[ERROR] %s\n" % str(self.message)

    def log(self):
        ret = "%s" % str(self.message)
        return ret


class SPAInitializationError(Error):
    """
    Raised when one or more required data for the SPA calculation are
    missing.
    """
    def __init__(self, message):
        self.message = message

    def __str__(self):
        ret = "[INIT_ERROR] %s\n" % str(self.message)
        return ret


class DataDimensionError(Error):
    """
    Raised when matrix dimensions of some parameters are such that matrix
    operations are not defined.
    """
    def __init__(self, message):
        self.message = message

    def __str__(self):
        ret = "[DIM_ERROR] %s\n" % str(self.message)
        return ret


class Process(object):

    def __init__(self, code, amt, price):
        self._code = code
        self._amt = amt
        self._price = price

    @property
    def code(self):
        return self._code

    @property
    def amt(self):
        return self._amt

    @property
    def price(self):
        return self._price

    @property
    def total_price(self):
        return self._amt * self._price


class Model_Generator(object):

    def __init__(self):
        self.p_in = {}
        self.dim = None
        self.v = None
        self.u = None
        self.b = None
        self.codes = None
        self.environmental_impact = None
        self.p_out = None
        # self.future = matlab.engine.start_matlab(async=True)

    def add_process_output(self, code, output, price):
        # Save process output values as 3-tuple
        self.p_out = Process(code, output, price)

    def add_process_input(self, code, input, price):
        if code in self.p_in:
            self.p_in[code].append(Process(code, input, price))
        else:
            self.p_in[code] = [Process(code, input, price)]

    def add_environmental_impact(self, amt):
        self.environmental_impact = amt

    def add_v(self, v_path):
        self.v = np.loadtxt(open(v_path, 'rb'), delimiter=',')
        if not _is_square(self.v):
            msg = 'v is not square, shape = {}'
            raise DataDimensionError(msg.format(self.v.shape))
        if self.dim is None:
            self.dim = len(self.v)
        else:
            if len(self.v) != self.dim:
                msg = 'dimensions of v ({}) do not match previous data ({})'
                raise DataDimensionError(msg.format(self.v.shape, self.dim))

    def add_u(self, u_path):
        self.u = np.loadtxt(open(u_path, 'rb'), delimiter=',')
        if not _is_square(self.u):
            msg = 'u is not square, shape = {}'
            raise DataDimensionError(msg.format(self.u.shape))
        if self.dim is None:
            self.dim = len(self.u)
        else:
            if len(self.u) != self.dim:
                msg = 'dimensions of u ({}) do not match previous data ({})'
                raise DataDimensionError(msg.format(self.u.shape, self.dim))

    def add_b(self, b_path):
        self.b = np.loadtxt(open(b_path, 'rb'), delimiter=',')
        if self.dim is None:
            self.dim = len(self.b)
        else:
            if len(self.b) != self.dim:
                msg = 'length of b ({}) does not match previous data ({})'
                raise DataDimensionError(msg.format(len(self.b), self.dim))

    def add_codes(self, codes_path):
        f = open(codes_path, 'r')
        line = f.readline()
        self.codes = line.split(',')
        if self.dim is None:
            self.dim = len(self.codes)
        else:
            if len(self.codes) != self.dim:
                msg = 'length of codes ({}) does not match previous data ({})'
                raise DataDimensionError(msg.format(len(self.codes), self.dim))

    def run_spa(self, code):
        # Switch through cases
        err_str = None
        if self.u is None:
            err_str = 'u'
        elif self.v is None:
            err_str = 'v'
        elif self.b is None:
            err_str = 'b'
        elif self.codes is None:
            err_str = 'codes'
        elif self.environmental_impact is None:
            err_str = 'environmental_impact'
        if err_str is not None:
            init_err = 'Must add {0} via add_{0} before running SPA'
            raise SPAInitializationError(init_err.format(err_str))

        if self.p_out is None:
            init_err = 'Must add process output via add_process_output'
            raise SPAInitializationError(init_err)

        # Check whether requested code is valid
        if code == self.p_out.code:
            location = len(self.codes)
        else:
            try:
                location = self.codes.index(code)
            except ValueError:
                raise Exception('Code {} not in codes list.'.format(code))

        # Check whether output process code is in codes list
        try:
            p_location = self.codes.index(self.p_out.code)
            b_val = self.b[p_location]
        except ValueError:
            p_location = None
            b_val = 0

        # Generate X_mu (input process vector)
        x_vec = []
        for p in self.codes:
            if p in self.p_in:
                a = sum([x.total_price for x in self.p_in[p]])
            else:
                a = 0
            x_vec.append(a)

        # If output process code was found in codes list, disaggregate V and U
        if p_location is not None:
            self.v[p_location][p_location] -= self.p_out.total_price
            for i in range(len(self.codes)):
                self.u[i][p_location] -= x_vec[i]

        # Rebuild V, U, and B
        n = len(self.codes)
        self.v = np.c_[self.v, np.zeros(n)]
        self.v = np.r_[self.v, [np.zeros(n + 1)]]
        self.v[n][n] = self.p_out.total_price
        self.u = np.c_[self.u, x_vec]
        self.u = np.r_[self.u, [np.zeros(n + 1)]]
        self.b = np.append(self.b,
                           self.environmental_impact / self.p_out.total_price)

        # Compute A matrix
        a = np.dot(self.u, np.linalg.inv(self.v.T))

        # Generate F vector
        f = np.zeros(n + 1)
        f[location] = 1.0

        # Get relevant identity matrix
        i = np.identity(n + 1)

        # Compute emissions via e = b * (i - a) ^ (-1) * f
        emissions = np.dot(self.b, np.dot(np.linalg.inv(i - a), f))
        print('emissions = {}'.format(emissions))

        # Cast A, B to MATLAB compatible types
        # a = matlab.double(a.tolist())
        # b = matlab.double(self.b.tolist())
        a = a.tolist()
        b = self.b.tolist()


        # Get/wait for asynchronous MATLAB engine start
        # eng = self.future.result()

        emissions = float(emissions)
        # eng.runprog(int(location + 1), emissions, a, b, int(n + 1), nargout=0)
        spa_python.run_prog(int(location + 1), emissions, a, b, int(n + 1), th=0.005)
        # ret = eng.runprog(int(location + 1), emissions, a, b, int(n + 1))
        # print(ret)


def _is_square(m):
    square = True
    length = len(m)
    for row in m:
        if len(row) != length:
            square = False
    return square
