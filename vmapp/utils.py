from . import config
from .vmman import VMware, VirtualBox

def get_all_vm_list():
    res = []
    for i in config:
        if i["type"] == "virtualbox":
            v = VirtualBox(url=i["resturl"])
            l = v.get_all_vm()
            res += l
        elif i["type"] == "vmware":
            v = VMware(url=i["resturl"], username=i["username"], password=i["password"])
            l = v.get_all_vm()
            res += l
        else:
            raise ValueError
    return res