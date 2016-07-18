import redis


class RedisClient(object):
    def __init__(self, use_proxy_ip):
        self.redis_client = {}
        self.redis_info = {}
        self.proxy_ip = {}
        self.use_proxy_ip = use_proxy_ip

    def init_connection(self, group_info, proxy_info):
        for proxy in proxy_info:
            proxy_id = proxy.get_proxy_id()
            data = proxy_id.split("_")
            prefix = data[0]
            id = int(data[1])
            proxy_addr = proxy.get_proxy_addr()
            data = proxy_addr.split(":")
            host = data[0]
            port = int(data[1])
            self.proxy_ip[id] = host

        for group in group_info:
            for server in group.get_server_info():
                type = server.get_server_type()
                group_id = server.get_group_id()
                addr = server.get_server_addr()
                if type == 'slave':
                    if self.redis_info.get(group_id) is None:
                        self.redis_info[group_id] = addr
                        data = addr.split(":")
                        host = data[0]
                        port = int(data[1])
                        if self.use_proxy_ip:
                            host = self.proxy_ip[group_id]
                        try:
                            self.redis_client[group_id] = redis.StrictRedis(host=host, port=port, db=0)
                        except Exception as e:
                            print e

        print 'init redis connection'

    def get_redis_info(self):
        return self.redis_info

    def get_search_key(self, search_key):
        data = search_key.split(" ")
        pattern = '*'
        for key in data:
            pattern = '%s%s%s' % (pattern, key, '*')
        return pattern

    def get_key(self, search_key):
        key_list = []
        pattern = self.get_search_key(search_key)
        for (key, value) in self.redis_client.items():
            keys = value.keys(pattern=pattern)
            for key_str in keys:
                redis_key = {}
                redis_key['addr'] = self.redis_info[key]
                redis_key['key'] = key_str
                redis_key['group'] = key
                key_list.append(redis_key)
        return key_list

    def get_key_type(self, group_id, search_key):
        client = self.redis_client[group_id]
        return client.type(search_key)

    def get_string_value(self, group_id, search_key):
        client = self.redis_client[group_id]
        return client.get(search_key)

    def get_zset_zcard(self, group_id, search_key):
        client = self.redis_client[group_id]
        return client.zcard(search_key)

    def get_zset_zrange(self, group_id, search_key, start, stop):
        client = self.redis_client[group_id]
        return client.zrange(search_key, start, stop)

