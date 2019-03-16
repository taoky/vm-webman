from requests import get, post, put
import configparser
from . import config


class Config:
    def __init__(self):
        self.config = configparser.ConfigParser().read("vmapp/config.ini")
        for i in self.config.sections():  # check valid values
            if 'type' not in i:
                raise ValueError("Please set VM type (\"vmware\" or \"virtualbox\").")
            type = i["type"]
            if type != "vmware" or type != "virtualbox":
                raise ValueError("Unsupported VM type.")
            if 'resturl' not in i:
                raise ValueError("Please set \"resturl\".")
            if type != "vmware" and ("username" not in i or "password" not in i):
                raise ValueError("For VMware RESTful API, a username and password is necessary.")


class VMManInterface:
    def get_all_vm(self):
        raise NotImplemented

    def get_one_vm_info(self, id):
        raise NotImplemented

    def update_one_vm_info(self, id, payload):
        raise NotImplemented

    def clone_one_vm(self):
        raise NotImplemented

    def delete_one_vm(self):
        raise NotImplemented

    def get_one_vm_power(self, id):
        raise NotImplemented

    def update_one_vm_power(self, id, operation):
        raise NotImplemented


class VMware(VMManInterface):
    def __init__(self, url, username, password):
        self.url = url
        self.username = username
        self.password = password

    def req(self, route, payload=None, method="get"):
        if method == "get":
            res = get(self.url + route, params=payload, auth=(self.username, self.password))
        elif method == "put":
            res = put(self.url + route, params=payload, auth=(self.username, self.password))
        else:
            res = post(self.url + route, params=payload, auth=(self.username, self.password))
        if res.status_code == 401:
            raise ValueError("Wrong username or password.")
        elif res.status_code != 200:
            raise ValueError("Get HTTP error %d" % res.status_code)
        return res.json()

    def get_all_vm(self):
        res = self.req("/vms")
        return [VM(id=i["id"], name=i["path"], type="vmware") for i in res]

    def get_one_vm_info(self, id):
        res = self.req("/vms/{}".format(id))
        return {"Processor Numbers": res["cpu"]["processors"], "Memory Size": res["memory"]}

    def get_one_vm_power(self, id):
        res = self.req("/vms/{}/power".format(id))
        return res["power_state"]

    def update_one_vm_power(self, id, operation):
        res = self.req("/vms/{}/power".format(id), method="get", payload={"operation": new_state})


class VirtualBox(VMManInterface):
    def __init__(self, url):
        self.url = url

    def req(self, route, payload=None, is_post=False):
        if not is_post:
            res = get(self.url + route, params=payload)
        else:
            res = post(self.url + route, params=payload)
        if res.status_code != 200:
            raise ValueError("Get HTTP error %d" % res.status_code)
        return res.json()

    def get_all_vm(self):
        res = self.req("/list/vms")
        return [VM(id=i["uuid"], name=i["name"], type="virtualbox") for i in res["list"]]

    def get_one_vm_info(self, id):
        res = self.req("/showvminfo/{}".format(id))
        return {"Memory": res["ram"], "Video Memory": res["vram"]}

    def get_one_vm_power(self, id):
        res = self.req("/showvminfo/{}".format(id))
        return res["state"]

    def update_one_vm_power(self, id, operation):
        if operation == "on":
            res = self.req("/startvm/{}".format(id))
        elif operation == "pause":
            res = self.req("/controlvm/{}/pause".format(id))
        elif operation == "unpause":
            res = self.req("/controlvm/{}/resume".format(id))
        elif operation == "off":
            res = self.req("/controlvm/{}/poweroff".format(id))
        else:
            raise ValueError("Unsupported operation.")


class VM:
    def __init__(self, id, name, type):
        self.id = id
        self.name = name
        self.type = type


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