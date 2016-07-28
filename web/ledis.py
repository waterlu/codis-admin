import redis


class RedisClient(object):
    def __init__(self, use_proxy_ip, max_count):
        self.redis_client = {}
        self.redis_info = {}
        self.proxy_ip = {}
        self.use_proxy_ip = use_proxy_ip
        self.max_count = max_count

    def reset(self, use_proxy_ip, max_count):
        self.redis_client = {}
        self.redis_info = {}
        self.proxy_ip = {}
        self.use_proxy_ip = use_proxy_ip
        self.max_count = max_count

    def get_max_count(self):
        return self.max_count

    def get_use_proxy_ip(self):
        return self.use_proxy_ip

    def find_group_id(self, addr):
        for (group_id, client) in self.redis_info.items():
            if (client == addr):
                return group_id
        return -1

    def init_connection(self, group_info, proxy_info):
        """

        :param group_info: the redis server information
        :param proxy_info: the codis proxy information
        :return:
        """
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
                        data = addr.split(":")
                        host = data[0]
                        port = int(data[1])
                        if self.use_proxy_ip:
                            host = self.proxy_ip[group_id]
                        self.redis_info[group_id] = '%s:%d' % (host, port)
                        try:
                            self.redis_client[group_id] = redis.StrictRedis(host=host, port=port, db=0)
                        except Exception as e:
                            print e

        print 'init redis connection'

    def get_redis_info(self):
        return self.redis_info

    def get_redis_client(self):
        return self.redis_client

    def get_search_key(self, search_key):
        """

        :param search_key: the key to query (fuzzy searching)
        :return: the pattern to search
        """
        data = search_key.split(" ")
        pattern = '*'
        for key in data:
            pattern = '%s%s%s' % (pattern, key, '*')
        return pattern

    def get_key(self, search_key, count):
        """

        :param search_key: the key to query (fuzzy searching)
        :return: all the keys match the query condition
        """
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
                if len(key_list) >= count:
                    return key_list
        return key_list

    def get_key_type(self, group_id, search_key):
        """

        :param group_id: to get the redis server
        :param search_key: the key
        :return: the type of the key
        """
        client = self.redis_client[group_id]
        return client.type(search_key)

    def string_get(self, group_id, search_key):
        """

        :param group_id: to get the redis server
        :param search_key: the key of the string
        :return: the value of the string
        """
        client = self.redis_client[group_id]
        return client.get(search_key)

    def zset_zcard(self, group_id, search_key):
        """

        :param group_id: to get the redis server
        :param search_key: the key of the sorted set
        :return: the count of the members in the sorted set
        """
        client = self.redis_client[group_id]
        return client.zcard(search_key)

    def zset_zrange(self, group_id, search_key, start, stop):
        """

        :param group_id: to get the redis server
        :param search_key: the key of the sorted set
        :param start: start position
        :param stop: end position
        :return: the members in the sorted set
        """
        client = self.redis_client[group_id]
        return client.zrange(search_key, start, stop)

    def set_scard(self, group_id, search_key):
        """

        :param group_id: to get the redis server
        :param search_key: the key of the set
        :return: the count of the members in the set
        """
        client = self.redis_client[group_id]
        return client.scard(search_key)

    def set_srandmember(self, group_id, search_key, count):
        """

        :param group_id: to get the redis server
        :param search_key: the key of the set
        :param count: one random member in the set
        :return:
        """
        client = self.redis_client[group_id]
        return client.srandmember(search_key, count)

    def set_smembers(self, group_id, search_key):
        """

        :param group_id: to get the redis server
        :param search_key: the key of the set
        :return: all the members in the set
        """
        client = self.redis_client[group_id]
        return client.smembers(search_key)