
    # set default path
    # path_config = PATH_CONFIG_DEF

    # # check if there is an arg for config path
    # if PATH_CONFIG_ARG in g_dict_args.keys():

    #     path_config = g_dict_args[PATH_CONFIG_ARG]
    #     if path_config is not None and path_config is not '':

    #         # load from the arg path
    #         path_config = g_dict_args[PATH_CONFIG_ARG]

    # # load config dict from file (or just keep built-in)
    # _load_config(path_config)

    # # declare config dict global BEFORE using it (even before reading?)
    # global g_dict_config

    # # create the app object
    # app = gui.App()

    # # get gui config dict and pass it to the app object
    # if 'gui' in g_dict_config.keys():
    #     app.set_gui(g_dict_config['gui'])

    # # show the window
    # app.run()

    # # get gui values/window state
    # a_dict = app.get_gui()

    # # set the gui stuff into the config dict
    # g_dict_config['gui'] = a_dict

    # # save config dict to file
    # _save_config(path_config)
