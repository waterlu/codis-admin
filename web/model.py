class User(object):
    def __init__(self, user_id, user_name):
        self.user_id = user_id
        self.user_name = user_name


class ServerInfo(object):
    def __init__(self, group_id, server_type, server_addr):
        self.server_type = server_type
        self.server_addr = server_addr
        self.group_id = group_id

    def get_group_id(self):
        return self.group_id

    def get_server_addr(self):
        return self.server_addr

    def get_server_type(self):
        return self.server_type


class GroupInfo(object):
    def __init__(self, group_id):
        self.group_id = group_id
        self.server_info = []

    def add_server(self, server_type, server_addr):
        server_info = ServerInfo(self.group_id, server_type, server_addr)
        self.server_info.append(server_info)

    def get_id(self):
        return self.group_id

    def get_server_info(self):
        return self.server_info

    def find_group_id(self, addr):
        for server_info in self.server_info:
            if server_info.get_server_addr() == addr:
                return server_info.get_group_id()
        return -1


class ProxyInfo(object):
    def __init__(self, proxy_id, proxy_addr, proxy_debug_var_addr, proxy_state):
        self.proxy_id = proxy_id
        self.proxy_addr = proxy_addr
        self.proxy_debug_var_addr = proxy_debug_var_addr
        self.proxy_state = proxy_state

    def get_proxy_id(self):
        return self.proxy_id

    def get_proxy_addr(self):
        return self.proxy_addr

    def get_proxy_debug_addr(self):
        return self.proxy_debug_var_addr

    def get_proxy_state(self):
        return self.proxy_state


class CodisInfo(object):
    def __init__(self):
        self.group_info = []
        self.proxy_info = []
        self.init = False

    def add_codis_server(self, group_id, server_type, server_addr):
        group_info = None
        for group in self.group_info:
            if group.get_id() == group_id:
                group_info = group
                break

        if group_info is None:
            group_info = GroupInfo(group_id)
            self.group_info.append(group_info)

        group_info.add_server(server_type, server_addr)

    def get_group_info(self):
        return self.group_info

    def add_proxy(self, proxy_id, proxy_addr, proxy_debug_var_addr, proxy_state):
        proxy_info = ProxyInfo(proxy_id, proxy_addr, proxy_debug_var_addr, proxy_state)
        self.proxy_info.append(proxy_info)

    def get_proxy_info(self):
        return self.proxy_info

    def has_init(self):
        return self.init

    def init_done(self):
        self.init = True

    def find_group_id(self, addr):
        for group_info in self.group_info:
            group_id = group_info.find_group_id(addr)
            if group_id > 0:
                return group_id
        return -1
