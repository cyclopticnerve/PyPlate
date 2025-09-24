# def change_d(global_d):
#     local_d = global_d.copy()
#     local_d["key"] = "foo"
#     return local_d

# global_d = {
#     "key": "value"
# }
# print(global_d)
# global_d = change_d(global_d)
# print(global_d)

# # ------------------------------------------------------------------------------

# def change_s(global_s):
#     local_s = str(global_s)
#     local_s = "World"
#     return local_s


# global_s = "Hello"
# print(global_s)
# global_s = change_s(global_s)
# print(global_s)

# ------------------------------------------------------------------------------

def change_d2(global_d):
    global_d["key"] = {"foo": "bar"}

global_d = {"key": {"key2": "val2"}}
global_d2 = global_d["key"]  # {"key2": "val2"}
print(global_d)  # {"key": {"key2": "val2"}}
print(global_d2)  # {"key2": "val2"}

change_d2(global_d)
# global_d2 = global_d["key"]
print(global_d)
print(global_d2)
