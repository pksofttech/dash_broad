from datetime import datetime
from logging import debug
from werkzeug.serving import make_server
from flask import Flask, render_template, redirect, request, Response
from flask_socketio import SocketIO, emit
from pprint import pprint
import threading
import os
import time


class ServerThread(threading.Thread):

    def __init__(self, app_name="Flask_Server", debug=True, syslog=None, port=80, host_ip="0.0.0.0", call_back=None):
        threading.Thread.__init__(self)
        print('Create Server...')
        self.app = Flask(app_name)
        self.app.config['SECRET_KEY'] = 'secret!'
        self.debug = debug
        self.syslog = syslog
        self.socketio = SocketIO(self.app)
        self.port = port
        self.host_ip = host_ip
        self.clients = []
        self.call_back = call_back

        @self.app.errorhandler(404)
        def page_not_found(error):
            return render_template('404.html', title='404'), 404

        @self.app.route('/')
        def index():
            return render_template('login.html')

        @self.app.route('/tables', methods=['GET', 'POST'])
        def tables():
            try:
                if(request.method == "GET"):
                    rows_count = request.args.get('rows')
                    if(rows_count == None):
                        rows_count = 100
                    rows = self.call_back(gettables=rows_count)
                    table_str = ""
                    for row in rows:
                        str_row = "<tr> <td>{}</td> <td>{}</td> <td>{}</td> </tr>".format(
                            row[0], row[1], row[2])
                        table_str += str_row
                    return render_template('tables.html', data_set=table_str, table_detail="{} แถว".format(len(rows)))
            except Exception as err:
                err

        @self.app.route('/charts')
        def charts():
            return render_template('charts.html')

        @self.app.route('/main', methods=['GET', 'POST', 'DELETE'])
        def index_main():
            try:
                if(request.method == "GET"):
                    print(
                        "-----------------------------------------------------------------GET")
                    _data = self.call_back(getdata="all")
                    print(_data)
                    #str_x = _data["x_line"]
                    # print(str_x)
                    return render_template("index.html",
                                           status=_data["status"],
                                           gate_01=_data["Gate_01"],
                                           gate_02=_data["Gate_02"],
                                           x_line=_data["x_line"],
                                           y_line01=_data["y_line01"],
                                           y_line02=_data["y_line02"],
                                           y_line03=_data["y_line03"],
                                           t_gate_01=_data["t_gate_01"],
                                           t_gate_02=_data["t_gate_02"],
                                           t_gate=_data["t_gate"],
                                           date_start=_data["date_start"],
                                           date_end=_data["date_end"])

                if(request.method == "POST"):
                    print(
                        "-----------------------------------------------------------------POST")
                    result = request.form
                    # pprint(result)
                    date_start = result.get("date_start")
                    date_end = result.get("date_end")
                    result = self.call_back(setdata={
                        "date_start": date_start,
                        "date_end": date_end})

                    return redirect('/main')

            except Exception as err:
                print("ERROR Server : {}".format(err))
                return(err)

        @self.app.route('/test', methods=['GET', 'POST'])
        def test():
            try:
                if(request.method == "GET"):
                    para = request.args.get('event')
                    print("Msg << {}".format(para))
                    if(para == "sw_01"):
                        result = self.call_back(event={"msg": para})
                    if(para == "sw_02"):
                        result = self.call_back(event={"msg": para})
                    return Response(" << OK : {}\r\n".format(para))
            except Exception as err:
                print("Error: {}".format(err))

# ? ---------------------- socketio -------------------------------------------#
        @self.socketio.on('connect')
        def test_connect():
            print(request.sid)
            self.clients.append(request.sid)
            emit('connect', "Connect...")

        @self.socketio.on('disconnect')
        def handle_disconnect():
            print('Client disconnected')
            self.clients.remove(request.sid)

    def send_message(self, msg, header="update", ):
        for client_id in self.clients:
            self.socketio.emit(header, str(msg), room=client_id)
            print('sending {}: message "{}" to client "{}".'.format(
                header, msg, client_id))

    def run(self):
        # if(self.syslog is not None):
        #    self.syslog.info('starting server')
        print('starting server')
        # self.srv.serve_forever()
        self.socketio.run(host=self.host_ip, port=self.port,
                          app=self.app, debug=False)

    def shutdown(self):
        # self.srv.shutdown()
        self.socketio.stop()
        if(self.syslog is not None):
            self.syslog.info('shutdown server')
        print('shutdown server')
