
dict_gui = {'entry': '', 'check': 'False'}

dict_in = {'entry': 'knob'}

for key in dict_gui.keys():
    if key not in dict_in.keys():
        dict_in[key] = dict_gui[key]

print(dict_in)
