import tools as t


if __name__ == '__main__':
    ds_v = t.Data('../data/sets/r1/', 'v.npy')
    ds_v.load_dataset()
    ds_v.prepare_dataset()
    t.display_data([ds_v], 1000, 1500)

    # t.display_data_in_rows([ds_v],
    #                        [1000],
    #                        [0])

    # ds_p = t.Data('../data/sets/r0/', 'p1.npy')
    # ds_t = t.Data('../data/sets/r0/', 't1.npy')
    #
    # ds_p.load_dataset()
    # ds_p.prepare_dataset(type='sfa-p')
    #
    # ds_t.load_dataset()
    # ds_t.prepare_dataset()
    #
    # _f_size = 2000
    # for _f_p_pos in range(0, 100000, 1500):
    #     sfa_p = t.SFAAlg(ds_p.pd, _f_p_pos, _f_size, 30)
    #     sfa_p.calculate_fourier_coefficients()
    #     t.display_data_in_rows([sfa_p.apml, sfa_p.phase, ds_p.pd],
    #                            [30, 30, _f_size],
    #                            [1, 1, _f_p_pos])
    #
    #