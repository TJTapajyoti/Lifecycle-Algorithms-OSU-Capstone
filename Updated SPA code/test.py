import python_wrapper as p

a = p.Model_Generator()
a.add_process_output('A03', 25, 1.5)
a.add_process_input('A01', 10.074, 3.0)
a.add_process_input('A02', 8.0592, 2.5)
a.add_environmental_impact(7.5)
a.add_v('v.csv')
a.add_u('u.csv')
a.add_b('b.csv')
a.add_codes('codes.csv')
a.run_spa('A03')
