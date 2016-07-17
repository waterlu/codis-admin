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


class CodisInfo(object):
    def __init__(self):
        self.group_info = []

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