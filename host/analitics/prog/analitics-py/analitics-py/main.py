import tools as t
import classifier as c
import configuration as conf
import analitics as a
import numpy as np

if __name__ == '__main__':
    normal = t.Data(conf.path, conf.data_set_type)
    normal.add_dataset_from_file('r2/normal/', 'normal', 'csv')

    timeout = t.Data(conf.path, conf.data_set_type)
    timeout.add_dataset_from_file('r2/normal/', 'timeout', 'csv')

    ds_sizes = 5000
    ds_pos = 0
    ds_power = []
    ds_power = np.append(ds_power,
                         t.prepare_dataset(normal.ods['Power'], ds_pos, ds_sizes, 'cut'))
    ds_power = np.append(ds_power,
                         t.prepare_dataset(timeout.ods['Power'], ds_pos, ds_sizes, 'cut'))

    ds_temperature = []
    ds_temperature = np.append(ds_temperature,
                               t.prepare_dataset(normal.ods['Temp'], ds_pos, ds_sizes, 'diff'))
    ds_temperature = np.append(ds_temperature,
                               t.prepare_dataset(timeout.ods['Temp'], ds_pos, ds_sizes, 'diff'))

    # t.plot_series(ds_power, 0, len(ds_power))
    # t.plot_series(ds_temperature, 0, len(ds_temperature))
    #
    # t.show_all_plots()

    CT = c.ClassificationTools(ds_power, ds_temperature)

    CT.define_power_classes()
    CT.define_temp_classes()

    classified_series = CT.apply_classes()

    print(classified_series)
    print(a.count_words(classified_series))

    CA = c.ClassesAnalytics(classified_series)

    CA.find_collections(classified_series, 6)

    val_pos = 5000
    val_size = 10000

    val_power = []
    val_power = np.append(val_power,
                          t.prepare_dataset(normal.ods['Power'], val_pos, val_size, 'cut'))

    val_temperature = []
    val_temperature = np.append(val_temperature,
                                t.prepare_dataset(normal.ods['Temp'], val_pos, val_size, 'diff'))



