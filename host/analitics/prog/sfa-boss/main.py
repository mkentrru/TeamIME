import tools as t


if __name__ == '__main__':
    ds_v = t.Data('../data/sets/r1/', 'v.npy')
    ds_v.load_dataset()
    ds_v.prepare_dataset()
    # ds_v.prepare_dataset()

    # t.display_data([ds_v], 0, 5000)


    # ds_p = t.Data('../data/sets/r0/', 'p1.npy')
    # ds_t = t.Data('../data/sets/r0/', 't1.npy')
    #
    # ds_p.load_dataset()
    # ds_p.prepare_dataset(type='sfa-p')
    #
    # ds_t.load_dataset()
    # ds_t.prepare_dataset()
    #
    coefficients_count = 30
    cut_position = 1000
    # row_length = 4500
    time_series_length = 500
    time_series_count = 3
    row_length = time_series_length * time_series_count
    sfa_p = t.SFAAlg(ds_v.pd, coefficients_count)

    sfa_p.transform(cut_position, row_length, time_series_length, time_series_count)

    # print(sfa_p.transformed.todense())

    t.display_single_data_in_rows(ds_v.pd,
                                  cut_position,
                                  time_series_length,
                                  time_series_count)

    sfa_p.display_bars()

    ds_v.plots_show()

    # t.display_data_in_rows([ds_v.pd for i in range(0, cuts_count)],
    #                        [200,        200,        200,        200,        200],
    #                        [0,          200,        400,        600,        800])
    # t.display_data_in_rows([sfa_p.apml, sfa_p.phase, ds_v.pd],
    #                        [4, 4, _f_size],
    #                        [0, 0, _f_p_pos])
