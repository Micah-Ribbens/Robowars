import pygame
# def copy_controlls(controlls):
#     copy = []
#     print("prevcopy: ", controlls[pygame.K_RIGHT])
#     for controll in controlls:
#         copy.append(controll)
#     return copy
def deepcopy(object):
    copied_object = type(object)()
    for key in copied_object.attributes:
        # if key == "controlls":
        #     copied_object.__dict__[key] = copy_controlls(object.__dict__[key])
        # else:
        copied_object.__dict__[key] = object.__dict__[key]

    return copied_object
