# VM Web Manager

(Python & Deep Learning 101, USTC, 2019 Spring)

Keyu Tao, PB17111630

---

## 介绍

本项目可用于远程的虚拟机（Virtual Machine）简单管理，支持 VMware（使用官方的 RESTful API）与 VirtualBox（使用 `vboxmanage-rest-api` from <https://github.com/papnkukn/vboxmanage-rest-api>）。包含以下特性：

- 支持基于配置文件，整合不同来源的、基于 HTTP 协议的虚拟机管理 API。
- 基于 Django 用户组，允许多种类型的用户：仅查看、查看并改变虚拟机电源状态、管理（使用 Django Admin 面板）。权限划分比原始的 API 更加细化。

用户可以：

- 查看虚拟机列表。
- 查看某个虚拟机的配置信息。
- 查看某个虚拟机的电源状态。
- 改变某个虚拟机的电源状态。

适用于此类的情景：例如，用户需要在外网对内网（如实验室）中的虚拟机进行简单的电源管理操作，但是无法将虚拟机提供的 RESTful API 直接暴露的情况。

在 Python 3.7，macOS 10.14.3，VMware Fusion 11.0.2，VirtualBox 6.0.4 下测试通过。

GitHub 不适合放置较大的二进制文件（不使用 LFS 的情况下），所以要求的小视频发布在了 <https://www.bilibili.com/video/av46592034/>。

## 配置

### VMware

需要手动启用 VMware Workstation 或 VMware Fusion 的 RESTful API 特性，详情可查看 [How does REST API work in VMware Fusion and VMware Workstation?](https://www.starwindsoftware.com/blog/how-does-rest-api-work-in-vmware-fusion-and-vmware-workstation)。

### VirtualBox

需要使用 `npm` 下载 `vboxmanage-rest-api`。之后，在终端中执行以下命令以启动 RESTful API 服务器：

```
vboxmanage-rest-api --port 8269 --verbose --vboxmanage /usr/local/bin/vboxmanage
```

其中 `--vboxmanage` 后接 `vboxmanage` 所在位置。**请注意：`vboxmanage-rest-api` 不支持密码验证，不要将此 API 暴露于公网中。**

### 项目配置

在虚拟环境中安装 `requirements.txt` 中的依赖（`pip install -r requirements.txt`），然后运行 `setup.py`，设置超级用户的用户名与密码（邮箱可以随便填）。

之后打开 `vmapp/config.ini`，根据您的设置，调整 API 的 URL 与用户名、密码（如果有）。最后执行 `python manage.py runserver`，启动服务器。

在浏览器中访问 `http://IP:Port/admin`，使用超级用户登录后可以使用 Django Admin 面板，可以新建用户。对于非 staff 和 superuser 用户，需要加入 `change_power_operation` 用户组以授予改变虚拟机电源状态的权限。

## 代码

主要部分在 Django App `vmapp` 下。

没有定义 Django model，因为虚拟机信息是实时访问 API 调取的，这里没有必要持久化到数据库中。主要代码在：

- `utils.py`：定义几个助手函数，以便 `views.py` 调用。
- `vmman.py`：定义了配置类（含配置文件校验）、虚拟机接口以及从虚拟机接口继承的两个类 `VirtualBox` 和 `VMware`，这两个类中对不同类型的虚拟机进行了处理，使用 `requests` 库实际访问 API 的代码即在类中。
- `views.py`：Django 的 MTV 架构中的 V 部分。处理用户的网络请求，并且返回相应的内容。

Django 模版、CSS 等文件放置于 `vmapp` 下的 `templates` 与 `static` 文件夹下。