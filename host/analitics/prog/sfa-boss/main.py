import numpy as np
import matplotlib.pyplot as plt
import tools as t


if __name__ == '__main__':
    # c = t.Configuration(2, 10)
    ds_p = t.Data('../data/sets/r0/', 'p1.npy')
    ds_t = t.Data('../data/sets/r0/', 't1.npy')
    # d.simulate_dataset(c.time_series_size, c.time_series_length, [30, 0.5])
    # d.save_dataset()

    ds_p.load_dataset()
    ds_p.prepare_dataset()

    ds_t.load_dataset()
    ds_t.prepare_dataset()

    _f_size = 100
    _f_p_pos = 0
    sfa_p = t.SFA(ds_p.ds, _f_p_pos, _f_size, 20)
    sfa_p.calculate_fourier_coefficients()

    sfa_t = t.SFA(ds_t.ds, _f_p_pos, _f_size, 20)
    sfa_t.calculate_fourier_coefficients()

    # t.display_data_in_rows([sfa_p, ds_p], [20 - 2, _f_size], [2, _f_p_pos],
    #                        ['g', 'b'])

    t.display_data_in_rows([sfa_t, ds_t], [20 - 2, _f_size], [2, _f_p_pos],
                           ['g', 'b'])

    # t.display_data([ds_p], 12000, 13000)
    # t.display_data([sfa_p, ds_p], 0, 300)
    # t.display_data([sfa_t, ds_t], 10, 300)
    # d.prepare_dataset()
