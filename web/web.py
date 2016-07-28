from flask import Flask, render_template, jsonify, request, abort
from model import CodisInfo
from ledis import RedisClient
import json

app = Flask(__name__)

zk_addr = "60.205.59.69:2181"
product_name = "test"
use_proxy_ip = True
max_count = 50

redis_client = RedisClient(use_proxy_ip, max_count)
codis_info = CodisInfo(zk_addr, product_name, redis_client)


@app.route('/')
def index():
    codis_info.init_codis_info()
    return render_template('index.html')


@app.route('/api/setting', methods=['GET'])
def get_setting():
    data = {}
    data['zk_addr'] = codis_info.get_zk_addr()
    data['product_name'] = codis_info.get_product_name()
    data['max_count'] = redis_client.get_max_count()
    data['use_proxy_ip'] = redis_client.get_use_proxy_ip()
    return jsonify({'data': data, 'errorCode': 0})


@app.route('/api/status', methods=['GET'])
def get_status():
    server_list = []
    client_info = redis_client.get_redis_client()
    redis_info = redis_client.get_redis_info()
    for (group_id, client) in client_info.items():
        server = {}
        server['group_id'] = group_id
        server['redis_server'] = redis_info[group_id]
        server_list.append(server)
    return jsonify({'data': server_list, 'errorCode': 0})


@app.route('/api/setting', methods=['POST'])
def change_setting():
    if not request.json:
        abort(400)
    zk_addr = request.json['zk_addr']
    product_name = request.json['product_name']
    max_count = request.json['max_count']
    use_proxy_ip = request.json['use_proxy_ip']
    redis_client.reset(use_proxy_ip, max_count)
    codis_info.reset(zk_addr, product_name, redis_client)
    codis_info.init_codis_info()

    data = {}
    server_list = []
    client_info = redis_client.get_redis_client()
    redis_info = redis_client.get_redis_info()
    for (group_id, client) in client_info.items():
        server = {}
        server['group_id'] = group_id
        server['redis_server'] = redis_info[group_id]
        server_list.append(server)
    data['zk_addr'] = codis_info.get_zk_addr()
    data['product_name'] = codis_info.get_product_name()
    data['max_count'] = redis_client.get_max_count()
    data['use_proxy_ip'] = redis_client.get_use_proxy_ip()
    data['servers'] = server_list
    return jsonify({'data': data, 'errorCode': 0})


@app.route('/api/proxy')
def codis_proxy():
    proxy_list = []
    for proxy_info in codis_info.get_proxy_info():
        proxy = {}
        proxy['id'] = proxy_info.get_proxy_id()
        proxy['addr'] = proxy_info.get_proxy_addr()
        proxy['debug_addr'] = proxy_info.get_proxy_debug_addr()
        proxy['state'] = proxy_info.get_proxy_state()
        proxy_list.append(proxy)
    proxy_info_json = json.dumps(proxy_list)
    return proxy_info_json


@app.route('/api/groups')
def codis_groups():
    group_list = []
    for group_info in codis_info.get_group_info():
        group = {}
        group['id'] = group_info.get_id()
        server_list = []
        for server_info in group_info.get_server_info():
            server = {}
            server['id'] = server_info.get_group_id()
            server['addr'] = server_info.get_server_addr()
            server['type'] = server_info.get_server_type()
            server_list.append(server)
        group['servers'] = server_list
        group_list.append(group)
    group_info_json = json.dumps(group_list)
    return group_info_json


@app.route('/api/redis')
def slaves():
    redis_info_json = json.dumps(redis_client.get_redis_info())
    return redis_info_json


@app.route('/api/search/<key>')
def search(key):
    try:
        key_list = []
        count = 0
        if len(key) < 5:
            return jsonify({'data': key_list, 'count': count, 'errorCode': 1,
                            'errorMsg': 'The key must contain at least 5 characters'})
        if key.find("*") >= 0:
            return jsonify({'data': key_list, 'count': count, 'errorCode': 2,
                            'errorMsg': 'The key must not contain *'})
        key_list = redis_client.get_key(key, max_count)
        count = len(key_list)
        if count > max_count:
            return jsonify({'data': key_list[0:max_count], 'count': count, 'errorCode': 0})
        else:
            return jsonify({'data': key_list, 'count': count, 'errorCode': 0})
    except Exception as e:
        print 'exception in search:' + e.message
        return jsonify({'data': [], 'count':0, 'errorCode': 99, 'errorMsg': e.message})


@app.route('/api/type/<addr>/<key>')
def type(addr, key):
    try:
        group_id = codis_info.find_group_id(addr)
        type = redis_client.get_key_type(group_id, key)
        return jsonify({'type': type, 'errorCode': 0})
    except Exception as e:
        print e
        return jsonify({'data': "", 'errorCode': 99, 'errorMsg': e.message})


@app.route('/api/string/get/<addr>/<key>')
def string_get(addr, key):
    try:
        group_id = codis_info.find_group_id(addr)
        value = redis_client.string_get(group_id, key)
        value = unicode(value, errors='ignore')
        return jsonify({'value': value, 'errorCode': 0})
    except Exception as e:
        print e
        return jsonify({'value': "", 'errorCode': 99, 'errorMsg': e})


@app.route('/api/zset/zcard/<addr>/<key>')
def zset_zcard(addr, key):
    try:
        group_id = codis_info.find_group_id(addr)
        value = redis_client.zset_zcard(group_id, key)
        return jsonify({'value': value, 'errorCode': 0})
    except Exception as e:
        print e
        return jsonify({'value': "", 'errorCode': 99, 'errorMsg': e})


@app.route('/api/zset/zrange/<addr>/<key>/<start>/<stop>')
def zset_zrange(addr, key, start, stop):
    try:
        group_id = codis_info.find_group_id(addr)
        data = redis_client.zset_zrange(group_id, key, start, stop)
        list = []
        for value in data:
            list.append(unicode(value , errors='ignore'))
            # row = {}
            # row['data'] = unicode(value , errors='ignore')
            # list.append(row)
        return jsonify({'value': list, 'errorCode': 0})
    except Exception as e:
        print e
        return jsonify({'value': "", 'errorCode': 99, 'errorMsg': e})


@app.route('/api/set/scard/<addr>/<key>')
def set_scard(addr, key):
    try:
        group_id = codis_info.find_group_id(addr)
        value = redis_client.set_scard(group_id, key)
        return jsonify({'value': value, 'errorCode': 0})
    except Exception as e:
        print e
        return jsonify({'value': "", 'errorCode': 99, 'errorMsg': e})


@app.route('/api/set/srandmember/<addr>/<key>/<count>')
def set_srandmember(addr, key, count):
    try:
        group_id = codis_info.find_group_id(addr)
        data = redis_client.set_srandmember(group_id, key, count)
        list = []
        for value in data:
            list.append(unicode(value, errors='ignore'))
        return jsonify({'value': list, 'errorCode': 0})
    except Exception as e:
        print e
        return jsonify({'value': "", 'errorCode': 99, 'errorMsg': e})


@app.route('/api/set/smembers/<addr>/<key>')
def set_smembers(addr, key):
    try:
        group_id = codis_info.find_group_id(addr)
        data = redis_client.set_smembers(group_id, key)
        list = []
        for value in data:
            list.append(unicode(value, errors='ignore'))
        return jsonify({'value': list, 'errorCode': 0})
    except Exception as e:
        print e
        return jsonify({'value': "", 'errorCode': 99, 'errorMsg': e})


# def init_codis_info():
#     if codis_info.has_init():
#         return
#
#     try:
#         # start zookeeper client
#         zk_client = KazooClient(hosts=zk_addr)
#         zk_client.start()
#
#         # get codis server information
#         zk_servers_dir = "/zk/codis/db_%s/servers" % product_name
#         for zk_server in zk_client.get_children(zk_servers_dir):
#             zk_server_path = '/'.join((zk_servers_dir, zk_server))
#             for server in zk_client.get_children(zk_server_path):
#                 server_path = '/'.join((zk_server_path, server))
#                 data, stat = zk_client.get(server_path)
#                 server_info = json.loads(data)
#                 group_id = server_info.get('group_id')
#                 server_type = server_info.get('type')
#                 server_addr = server_info.get('addr')
#                 codis_info.add_codis_server(group_id, server_type, server_addr)
#
#         # get codis proxy information
#         zk_proxy_dir = "/zk/codis/db_%s/proxy" % product_name
#         for zk_proxy in zk_client.get_children(zk_proxy_dir):
#             zk_proxy_path = '/'.join((zk_proxy_dir, zk_proxy))
#             data, stat = zk_client.get(zk_proxy_path)
#             proxy_info = json.loads(data)
#             codis_info.add_proxy(proxy_info['id'], proxy_info['addr'], proxy_info['debug_var_addr'], proxy_info['state'])
#
#         redis_client.init_connection(codis_info.get_group_info(), codis_info.get_proxy_info())
#         codis_info.init_done()
#         return None
#     except Exception as e:
#         print e
#         return e


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=19080)
