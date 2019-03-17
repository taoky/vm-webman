from . import config
from .vmman import VMware, VirtualBox


def get_all_vm_list():
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
    if type == "virtualbox":
        v = VirtualBox(url=config[section]["resturl"], section=section)
        return v.update_one_vm_power(id, operation)
    elif type == "vmware":
        v = VMware(url=config[section]["resturl"], username=config[section]["username"],
                   password=config[section]["password"], section=section)
        return v.update_one_vm_power(id, operation)
    else:
        raise ValueError


def can_change_power_permission(user):
    return user.groups.filter(name="change_power_operation").exists() or user.is_staff or user.is_superuser
