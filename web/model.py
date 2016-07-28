from kazoo.client import KazooClient
import json

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
    def __init__(self, zk_addr, product_name, redis_client):
        self.group_info = []
        self.proxy_info = []
        self.zk_addr = zk_addr
        self.product_name = product_name
        self.redis_client = redis_client
        self.init = False

    def reset(self, zk_addr, product_name, redis_client):
        self.group_info = []
        self.proxy_info = []
        self.zk_addr = zk_addr
        self.product_name = product_name
        self.redis_client = redis_client
        self.init = False

    def get_zk_addr(self):
        return self.zk_addr

    def get_product_name(self):
        return self.product_name

    def init_codis_info(self):
        if self.has_init():
            return

        # start zookeeper client
        zk_client = KazooClient(hosts=self.zk_addr)
        zk_client.start()

        # get codis server information
        zk_servers_dir = "/zk/codis/db_%s/servers" % self.product_name
        for zk_server in zk_client.get_children(zk_servers_dir):
            zk_server_path = '/'.join((zk_servers_dir, zk_server))
            for server in zk_client.get_children(zk_server_path):
                server_path = '/'.join((zk_server_path, server))
                data, stat = zk_client.get(server_path)
                server_info = json.loads(data)
                group_id = server_info.get('group_id')
                server_type = server_info.get('type')
                server_addr = server_info.get('addr')
                self.add_codis_server(group_id, server_type, server_addr)

        # get codis proxy information
        zk_proxy_dir = "/zk/codis/db_%s/proxy" % self.product_name
        for zk_proxy in zk_client.get_children(zk_proxy_dir):
            zk_proxy_path = '/'.join((zk_proxy_dir, zk_proxy))
            data, stat = zk_client.get(zk_proxy_path)
            proxy_info = json.loads(data)
            self.add_proxy(proxy_info['id'], proxy_info['addr'], proxy_info['debug_var_addr'], proxy_info['state'])

        self.redis_client.init_connection(self.get_group_info(), self.get_proxy_info())
        self.init_done()
        return None

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
        return self.redis_client.find_group_id(addr)
        # for group_info in self.group_info:
        #     group_id = group_info.find_group_id(addr)
        #     if group_id > 0:
        #         return group_id
        # return -1
