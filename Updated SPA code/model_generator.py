from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
import numpy as np
from math import sqrt
from numpy.linalg import inv


class Model(object):

    def __init__(self, matrix, basis, impact, uncertainty_p, uncertainty_e,
                 complexity):
        self.matrix = matrix
        self.basis = basis
        self.impact = impact
        self.uncertainty_p = uncertainty_p
        self.uncertainty_e = uncertainty_e
        self.complexity = complexity

    def has_process(self, code):
        if code in self.basis:
            return True
        else:
            return False

    def has_process_input(self, output_code, input_code):
        if output_code not in self.basis:
            return False
        if input_code not in self.basis:
            return False
        row = self.basis.index(input_code)
        col = self.basis.index(output_code)
        if self.matrix[row][col] != 0:
            return True
        else:
            return False


class Output_Process(object):

    def __init__(self, code, value, env_impact, uncertainty_p, uncertainty_e,
                 complexity):
        self.code = code
        self.value = value
        self.env_impact = env_impact
        self.uncertainty_p = uncertainty_p
        self.uncertainty_e = uncertainty_e
        self.complexity = complexity


class Input_Process(object):

    def __init__(self, input_code, output_code, val):
        self.input_code = input_code
        self.output_code = output_code
        self.val = val


class Final_Model_Generator(object):

    def __init__(self, limit_c, uncertainty, limit_u):
        self.cur_model = Model([[]], [], [], [], [], [])
        self.next_model = None
        self.outputs = {}
        self.inputs = {}
        self.fail_counter = 0
        self.limit_c = float(limit_c)
        self.limit_u = float(limit_u)
        self.cur_rsd = None
        self.next_rsd = None
        self.uncertainty = float(uncertainty)
        # print('{} {} {}'.format(limit_c, uncertainty, limit_u))

    def add_process(self, code, value, env_impact, uncertainty_p=None,
                    uncertainty_e=None, complexity=None):
        print(env_impact)
        self.outputs[code] = Output_Process(code, value, env_impact,
                                            uncertainty_p, uncertainty_e,
                                            complexity)

    def add_process_input(self, output_code, input_code, value):
        self.inputs[(input_code, output_code)] = Input_Process(input_code,
                                                               output_code,
                                                               value)

    def has_process(self, code):
        boolean = code in self.outputs or self.cur_model.has_process(code)
        return boolean

    def has_process_input(self, output_code, input_code):
        boolean = (input_code, output_code) in self.inputs or \
                   self.cur_model.has_process_input(output_code, input_code)
        return boolean

    def set_process_unc_and_comp(self, code, uncertainty_p=None,
                                 uncertainty_e=None,
                                 complexity=None):
        if uncertainty_p is not None:
            self.outputs[code].uncertainty_p = uncertainty_p
        if uncertainty_e is not None:
            self.outputs[code].uncertainty_e = uncertainty_e
        if complexity is not None:
            self.outputs[code].complexity = complexity

    def create_new_matrix_and_calculate(self):
        old_matrix = np.array(self.cur_model.matrix)
        basis = np.array(self.cur_model.basis).tolist()
        env_impact = np.array(self.cur_model.impact).tolist()
        uncertainty_p = np.array(self.cur_model.uncertainty_p).tolist()
        uncertainty_e = np.array(self.cur_model.uncertainty_e).tolist()
        complexity = np.array(self.cur_model.complexity).tolist()
        for output in self.outputs:
            # print(basis)
            # print(env_impact)
            # print(uncertainty_e)
            # print(uncertainty_p)
            # print(complexity)
            output_proc = self.outputs[output]
            basis.insert(0, output)
            env_impact.insert(0, output_proc.env_impact)
            uncertainty_p.insert(0, output_proc.uncertainty_p)
            uncertainty_e.insert(0, output_proc.uncertainty_e)
            complexity.insert(0, output_proc.complexity)

        # create new matrix
        matrix = np.zeros((len(basis), len(basis)))
        # print(matrix)
        # print(basis)
        # print(env_impact)
        # print(uncertainty_e)
        # print(uncertainty_p)
        # print(complexity)

        # put old matrix in bottom right of new matrix
        if old_matrix.shape != (1, 0):
            matrix[-old_matrix.shape[0]:, -old_matrix.shape[1]:] = old_matrix

        # print(matrix)
        # print(basis)
        # print(env_impact)
        # print(uncertainty_e)
        # print(uncertainty_p)
        # print(complexity)

        # add diagonal elements
        for i in range(len(self.outputs)):
            output = basis[i]
            matrix[i][i] = float(self.outputs[output].value)

        # print(matrix)
        # print(basis)
        # print(env_impact)
        # print(uncertainty_e)
        # print(uncertainty_p)
        # print(complexity)

        # add off-diagonal elements that are defined
        for key in self.inputs:
            input_proc = self.inputs[key]
            output_code = input_proc.output_code
            input_code = input_proc.input_code
            row = basis.index(input_code)
            col = basis.index(output_code)
            matrix[row][col] = float(-1 * input_proc.val)

        # print(matrix)
        # print(basis)
        # print(env_impact)
        # print(uncertainty_e)
        # print(uncertainty_p)
        # print(complexity)

        # Save as next model
        self.next_model = Model(matrix, basis, env_impact, uncertainty_p,
                                uncertainty_e, complexity)

        # do error calculation here
        err_matrix = matrix.tolist()
        for i in range(len(err_matrix)):
            for j in range(len(err_matrix)):
                if matrix[i][j] != 0:
                    err_matrix[i][j] = uncertainty_p[j]
        err_matrix = np.array(err_matrix)

        F = [0 for x in env_impact]
        F[-1] = 1

        # print(matrix)
        # print(basis)
        # print(env_impact)
        # print(uncertainty_e)
        # print(uncertainty_p)
        # print(complexity)
        # print(err_matrix)
        # print(F)

        emission, SD, rsd = uncertainty(matrix, env_impact, F, err_matrix,
                                        uncertainty_e)

        boolean = True

        print(rsd)

        if sum(complexity) > self.limit_c:
            print('complexity fail')
            boolean = False

        if self.cur_rsd is not None:
            rsd_diff = rsd - self.cur_rsd
            if rsd_diff >= 0.0:
                print('resid diff: {}'.format(rsd_diff))
                print('resid 1 fail')
                boolean = False
            elif -1 * rsd_diff < self.limit_u:
                print('resid diff: {}'.format(rsd_diff))
                print('resid 2 fail')
                boolean = False
            else:
                self.next_rsd = rsd
        else:
            self.next_rsd = rsd

        if rsd < self.uncertainty:
            # print(rsd)
            # print(self.uncertainty)
            # print('{}'.format(rsd < self.uncertainty))
            print('succeed')
            self.cur_model = self.next_model
            boolean = 'exit'

        if not boolean:
            self.fail_counter += 1
            if self.fail_counter >= 5:
                boolean = 'exit'

        # return accept or reject
        return boolean

    def clear_unfinalized_data(self):
        self.next_model = None
        self.outputs = {}
        self.inputs = {}
        self.fail_counter += 1

    def finalize(self):
        if self.next_model is None:
            raise Exception('New matrix was not created')
        self.cur_model = self.next_model
        self.next_model = None
        self.outputs = {}
        self.inputs = {}
        self.fail_counter = 0
        self.cur_rsd = self.next_rsd
        self.next_rsd = None

    def get_most_recent_model(self):
        return self.cur_model


def uncertainty(X, M, F, sa, sb):
    t2 = np.dot(inv(X), M)
    t1 = np.dot(inv(X), F)
    term1 = 0
    for i in range(len(X)):
        term1 += (t1[i] * t1[i]) * (sb[i]**2)
    term2 = 0
    for i in range(len(X)):
        for j in range(len(X)):
            term2 += ((t2[i] * t1[j])**2) * (sa[i][j]**2)
    emission = np.dot(np.dot(inv(X), F), M)
    SD = sqrt(term2 + term1)
    if emission == 0:
        rsd = 0
    else:
        rsd = sqrt(term2 + term1) / emission
    return emission, SD, rsd
