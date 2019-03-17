from . import config
from .vmman import VMware, VirtualBox


def get_all_vm_list():
    """
    Get all virtual machines according to the config file.
    :return: list
    """
    res = []
    for key, value in config.items():
        if value["type"] == "virtualbox":
            v = VirtualBox(url=value["resturl"], section=key)
            l = v.get_all_vm()
            res += l
        elif value["type"] == "vmware":
            v = VMware(url=value["resturl"], username=value["username"], password=value["password"], section=key)
            l = v.get_all_vm()
            res += l
        else:
            raise ValueError
    return res


def get_one_vm_detail(id, type, section):
    """
    Get the detail of one vm according to its id, type and the section in config
    :param id: str
    :param type: str
    :param section: str
    :return: str (virtualbox) or dict (vmware)
    """
    if type == "virtualbox":
        v = VirtualBox(url=config[section]["resturl"], section=section)
        return v.get_one_vm_info(id)
    elif type == "vmware":
        v = VMware(url=config[section]["resturl"], username=config[section]["username"],
                   password=config[section]["password"], section=section)
        return v.get_one_vm_info(id)
    else:
        raise ValueError


def get_one_vm_state(id, type, section):
    """
    Get the vm power state.
    :param id: str
    :param type: str
    :param section: str
    :return: str
    """
    if type == "virtualbox":
        v = VirtualBox(url=config[section]["resturl"], section=section)
        return v.get_one_vm_power(id)
    elif type == "vmware":
        v = VMware(url=config[section]["resturl"], username=config[section]["username"],
                   password=config[section]["password"], section=section)
        return v.get_one_vm_power(id)
    else:
        raise ValueError


def update_one_vm_state(id, type, section, operation):
    """
    Update the vm power state. Permission is checked beforehand.
    :param id: str
    :param type: str
    :param section: str
    :param operation: str
    :return: None
    """
    if type == "virtualbox":
        v = VirtualBox(url=config[section]["resturl"], section=section)
        v.update_one_vm_power(id, operation)
    elif type == "vmware":
        v = VMware(url=config[section]["resturl"], username=config[section]["username"],
                   password=config[section]["password"], section=section)
        v.update_one_vm_power(id, operation)
    else:
        raise ValueError


def can_change_power_permission(user):
    """
    Check permission: whether this user can modify power state.
    :param user: django.contrib.auth.models.User
    :return: Bool
    """
    return user.groups.filter(name="change_power_operation").exists() or user.is_staff or user.is_superuser
