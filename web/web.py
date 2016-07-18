from flask import Flask, render_template, jsonify
from model import CodisInfo
from ledis import RedisClient
from kazoo.client import KazooClient
import json

app = Flask(__name__)

zk_addr = "60.205.59.69:2181"
product_name = "test"
use_proxy_ip = True
key_list = []
max_in_one_page = 5

codis_info = CodisInfo()
redis_client = RedisClient(use_proxy_ip)


@app.route('/')
def index():
    init_codis_info()
    return render_template('index.html')


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


@app.route('/api/search/<key>')
def search(key):
    key_list = redis_client.get_key(key)
    count = len(key_list)
    if count > max_in_one_page:
        page = count / max_in_one_page
        if count % max_in_one_page != 0:
            page = page + 1
        return jsonify({'data':key_list[0 : 5], 'page':page})
    else:
        return jsonify({'data':key_list[0 : 5], 'page':1})
    # key_info_json = json.dumps(key_list)
    # return key_info_json


@app.route('/api/redis')
def slaves():
    redis_info_json = json.dumps(redis_client.get_redis_info())
    return redis_info_json

def init_codis_info():
    if codis_info.has_init():
        return

    try:
        # start zookeeper client
        zk_client = KazooClient(hosts=zk_addr)
        zk_client.start()

        # get codis server information
        zk_servers_dir = "/zk/codis/db_%s/servers" % product_name
        for zk_server in zk_client.get_children(zk_servers_dir):
            zk_server_path = '/'.join((zk_servers_dir, zk_server))
            for server in zk_client.get_children(zk_server_path):
                server_path = '/'.join((zk_server_path, server))
                data, stat = zk_client.get(server_path)
                server_info = json.loads(data)
                group_id = server_info.get('group_id')
                server_type = server_info.get('type')
                server_addr = server_info.get('addr')
                codis_info.add_codis_server(group_id, server_type, server_addr)

        # get codis proxy information
        zk_proxy_dir = "/zk/codis/db_%s/proxy" % product_name
        for zk_proxy in zk_client.get_children(zk_proxy_dir):
            zk_proxy_path = '/'.join((zk_proxy_dir, zk_proxy))
            data, stat = zk_client.get(zk_proxy_path)
            proxy_info = json.loads(data)
            codis_info.add_proxy(proxy_info['id'], proxy_info['addr'], proxy_info['debug_var_addr'], proxy_info['state'])

        redis_client.init_connection(codis_info.get_group_info(), codis_info.get_proxy_info())
        codis_info.init_done()
    except Exception as e:
        print e


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=19080)
