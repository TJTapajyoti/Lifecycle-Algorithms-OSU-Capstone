from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
import matlab.engine
import numpy as np
import csv


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

    def add_process_output(self, code, output, price):
        # Save process output values as 3-tuple
        self.p_out = Process(code, output, price)

    def add_process_input(self, code, input, price):
        self.p_in[code] = Process(code, input, price)

    def add_environmental_impact(self, amt):
        self.env_impact = amt

    def add_v(self, v_path):
        self.v = np.loadtxt(open(v_path, "rb"), delimiter=",")

    def add_u(self, u_path):
        self.u = np.loadtxt(open(u_path, "rb"), delimiter=",")

    def add_b(self, b_path):
        self.b = np.loadtxt(open(b_path, "rb"), delimiter=",")

    def add_codes(self, codes_path):
        reader = csv.reader(open(codes_path, "r"), delimiter=",")
        self.codes = list(reader)
        self.codes = self.codes[0]

    def run_spa(self, code):

        # Check whether requested code is valid
        if code == self.p_out.code:
            location = len(self.codes)
        else:
            try:
                location = self.codes.index(code)
            except ValueError:
                raise Exception("Code {} not in codes list.".format(code))

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
                a = self.p_in[p].total_price
            else:
                a = 0
            x_vec.append(a)

        # If output process code was found in codes list, disaggregate
        if p_location is not None:
            self.v[p_location][p_location] -= self.p_out.total_price
            for i in range(len(self.codes)):
                self.u[i][p_location] -= x_vec[i]

        # Rebuild
        n = len(self.codes)
        self.v = np.c_[self.v, np.zeros(n)]
        self.v = np.r_[self.v, [np.zeros(n + 1)]]
        self.v[n][n] = self.p_out.total_price
        self.u = np.c_[self.u, x_vec]
        self.u = np.r_[self.u, [np.zeros(n + 1)]]
        self.b = np.append(self.b, self.env_impact / self.p_out.total_price)
        print('sec1 = {}'.format(location + 1))
        print('b = {}'.format(self.b))

        a = np.dot(self.u, np.linalg.inv(self.v.T))
        print('a = {}'.format(a))
        f = np.zeros(n + 1)
        f[location] = 1.0
        print('f = {}'.format(f))
        i = np.identity(n + 1)

        emissions = np.dot(self.b, np.dot(np.linalg.inv(i - a), f))
        print('emissions = {}'.format(emissions))
        print('nsec = {}'.format(n + 1))

        eng = matlab.engine.start_matlab()
        a = matlab.double(a.tolist())
        b = matlab.double(self.b.tolist())
        print(a)
        print(b)
        emissions = float(emissions)
        eng.runprog(int(location + 1),
                    emissions,
                    a,
                    b,
                    int(n + 1),
                    nargout=0)
