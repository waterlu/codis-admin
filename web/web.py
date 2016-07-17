from flask import Flask, render_template
from model import User, CodisInfo
from kazoo.client import KazooClient
import json

app = Flask(__name__)


@app.route('/')
def hello_world():
    codis_info = CodisInfo()
    zk_client = KazooClient(hosts="54.238.249.58:19181")
    zk_client.start()
    zk_servers_dir = "/zk/codis/db_cuet/servers"
    for child in zk_client.get_children(zk_servers_dir):
        child_path = '/'.join((zk_servers_dir, child))
        for server in zk_client.get_children(child_path):
            server_path = '/'.join((child_path, server))
            data, stat = zk_client.get(server_path)
            server_info = json.loads(data)
            codis_info.add_codis_server(server_info['group_id'], server_info['type'], server_info['addr'])

    return render_template('index.html', groups=codis_info.get_group_info())


@app.route('/user')
def user():
    user = User(1, 'Tom')
    return render_template('index.html', user=user)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=19080)
