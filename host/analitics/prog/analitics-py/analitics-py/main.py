import tools as t
import classifier as c
import configuration as conf
import analitics as a


if __name__ == '__main__':
    normal = t.Data(conf.path, conf.data_set_type)
    normal.add_dataset_from_file('r2/normal/', 'normal', 'csv')

    # t.plot_series(normal.ods['Power'], 0, 30000, 1)
    # t.plot_series(normal.ods['Temp'], 0, 30000, 1)

    ds_cut_pos = 0
    ds_cut_length = 30000

    ds_power = t.prepare_dataset(normal.ods['Power'],
                                 ds_cut_pos, ds_cut_length, 'cut')
    ds_temperature = t.prepare_dataset(normal.ods['Temp'],
                                       ds_cut_pos, ds_cut_length, 'diff')

    CT = c.ClassificationTools(ds_power, ds_temperature)

    tmp_size = 29000

    t.plot_series(normal.ods['Power'], 0, tmp_size, 1, 100)
    t.plot_series(normal.ods['Temp'], 0, tmp_size, 1, 100)

    CT.define_power_classes(0, tmp_size, 1)  # !!!
    CT.define_temp_classes(0, tmp_size, 1)

    classified_series = CT.apply_classes(0, tmp_size)

    print(classified_series)
    print(a.count_words(classified_series))

    CA = c.ClassesAnalytics(classified_series)

    CA.count_followings()

    # t.show_all_plots()

    # class_preprocessed = c.ClassifierPreprocessing(n_bins=4, word_size=2)
    #
    # # coefs = class_prepr.apply_transformation(pure_data.ods['Voltage'], 0, 500, 5)
    # # print(len(class_prepr.get_vocabulary()), ': ', class_prepr.get_vocabulary().values())
    # # print(coefs)
    # #
    # t.plot_series(pure_data.ods['Voltage'], 0, 200, 5)
    # t.show_all_plots()
    # # t.bar_series(coefs.toarray())
    #
    # class_learn = c.ClassifierLearning(conf.classifier_set_type)
    # class_learn.pick_learning_dataset(pure_data.ods, 'Voltage',
    #                                   0, 500, 250, 10000000, class_preprocessed)
