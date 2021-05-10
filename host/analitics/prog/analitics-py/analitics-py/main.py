import tools as t
import classifier as c
import configuration as conf


if __name__ == '__main__':
    normal = t.Data(conf.path, conf.data_set_type)
    normal.add_dataset_from_file('r1/', 'normal', 'csv')

    ABC = c.AverageBasedClassification(normal.ods['Power'])
    ABC.define_primary_classes(0, 1000, 1)

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
