from flask import Flask, render_template, current_app, request, jsonify, redirect, url_for, session
from flask_login import login_required, login_user, LoginManager, UserMixin, current_user, logout_user
from flask_socketio import SocketIO, emit
from flask_sqlalchemy import Model, SQLAlchemy
from random import choice
from random import sample
from time import time
import datetime
from send import send_finish_sms, send_receive_sms, send_problem_sms

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Hu3t C4 Pc s3Rv1c3!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pc_service.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
socketio = SocketIO(app, async_mode=None)
login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(userid):
    return User.get(userid)


@app.route('/', methods=['GET'])
def index():
    e = Event.query.filter_by(active=True).first()
    if e.running == 0:
        message = "%s %s 预约中" % (e.time, e.location)
    elif e.running == 1:
        message = "%s %s 进行中" % (e.time, e.location)
    else:
        message = "%s %s 已结束，暂无下一场活动安排" % (e.time, e.location)
    color = choice(['#efc5ca', '#c5cfef', '#c5efea', '#deefc5', '#efdfc5', '#efd2c5'])
    form = {
        'name': '',
        'tel': '',
        'model': '',
        'method': '',
        'other': '',
    }
    success = False
    if session.get('success', False):
        success = True
        session['success'] = False
    return render_template('index.html', form=form, color=color, success=success,
                           message=message,
                           disabled=(e.running == 2)
                           )


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    @staticmethod
    def get(uid):
        return User.query.get_or_404(uid)


class Ticket(db.Model):
    __tablename__ = 'tickets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10))
    tel = db.Column(db.String(11))
    method = db.Column(db.String(10))
    model = db.Column(db.String(20))
    other = db.Column(db.String)
    status = db.Column(db.Integer)
    comment = db.Column(db.String)
    short = db.Column(db.String(8))
    time = db.Column(db.Integer, default=time)
    event = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)


class SMS(db.Model):
    __tablename__ = 'SMS'
    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('tickets.id'), nullable=False)
    ticket = db.relationship('Ticket', backref=db.backref('tickets', lazy=True))
    content = db.Column(db.String)


class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(20))
    time = db.Column(db.String(40))
    active = db.Column(db.Boolean, default=True)
    running = db.Column(db.Integer, default=0)


@app.route('/', methods=['POST'])
def index_p():
    color = choice(['#efc5ca', '#c5cfef', '#c5efea', '#deefc5', '#efdfc5', '#efd2c5'])
    data = dict(request.form)
    wrong = dict()
    if len(data['name'][0]) < 2:
        wrong['name'] = '喵喵喵？听说你叫这个？ %s' % (data['name'][0])
    if len(data['tel'][0]) != 11 or str(int(data['tel'][0])).__len__() != 11:
        wrong['tel'] = '手机号写的不对，通知不到您呀！'
    if len(data['model'][0]) < 2:
        wrong['model'] = '型号写好，别被别人拿错啦！'
    if len(data.get('method', [])) < 1:
        wrong['method'] = '不告诉人家怎么修嘛！'
    if len(wrong):
        return render_template('index.html', wrong=wrong, form=data, color=color)
    code = ''.join(sample('1234567890', 6) )
    while Ticket.query.filter_by(short=code).first() is not None:
        code = ''.join(sample('1234567890', 6))
    e = Event.query.filter_by(active=True).first().id
    ticket = Ticket(name=data['name'][0],
                    tel=data['tel'][0],
                    method=''.join([a+',' for a in data['method']]),
                    model=data['model'][0],
                    other=data['other'][0],
                    status=0,
                    short=code,
                    event=e
                    )
    db.session.add(ticket)
    db.session.commit()
    send_list()
    session['success'] = True
    return redirect('/')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin'))
    if request.method == 'GET':
        csrf = ''.join(sample("abcdefghijklmnopqrstuvwxyz123456789", 30))
        try:
            current_app.csrf_token.append(csrf)
        except:
            current_app.csrf_token = []
        return render_template('login.html', csrf=csrf)
    data = request.form
    if data['csrf'] not in current_app.csrf_token:
        return '你想干嘛？'
    current_app.csrf_token.remove(data['csrf'])
    user = User.query.filter_by(username=data['username'], password=data['password']).first()
    if user is not None:
        login_user(user)
        return redirect(url_for('admin'))

    csrf = ''.join(sample("abcdefghijklmnopqrstuvwxyz123456789", 30))
    try:
        current_app.csrf_token.append(csrf)
    except:
        current_app.csrf_token = []
    return render_template('login.html', csrf=csrf)


@socketio.on('receive', namespace='/manage')
def receive(data):
    ticket = Ticket.query.filter_by(short=data['id']).first()
    ticket.status = 1
    db.session.add(ticket)
    db.session.commit()
    send_list()
    send_receive_sms(ticket.tel, ticket.short)


@socketio.on('start', namespace='/manage')
def receive(data):
    ticket = Ticket.query.filter_by(short=data['id']).first()
    ticket.status = 2
    db.session.add(ticket)
    db.session.commit()
    send_list()


@socketio.on('finish', namespace='/manage')
def receive(data):
    ticket = Ticket.query.filter_by(short=data['id']).first()
    ticket.status = 3
    db.session.add(ticket)
    db.session.commit()
    send_list()
    send_finish_sms(ticket.tel, ticket.short)


@socketio.on('problem', namespace='/manage')
def receive(data):
    ticket = Ticket.query.filter_by(short=data['id']).first()
    ticket.status = 5
    ticket.other += '=-=****Problem: \n' + data.get('problem', 'None') + '****=-='
    db.session.add(ticket)
    db.session.commit()
    send_list()
    send_problem_sms(ticket.tel, data.get('problem', 'N/A'))


@socketio.on('sent', namespace='/manage')
def receive(data):
    ticket = Ticket.query.filter_by(short=data['id']).first()
    ticket.status = 4
    db.session.add(ticket)
    db.session.commit()
    send_list()


@socketio.on('repairing', namespace='/manage')
def receive(data):
    ticket = Ticket.query.filter_by(short=data['id']).first()
    ticket.status = 2
    db.session.add(ticket)
    db.session.commit()
    send_list()


@socketio.on('reject', namespace='/manage')
def receive(data):
    ticket = Ticket.query.filter_by(short=data['id']).first()
    ticket.status = 98
    db.session.add(ticket)
    db.session.commit()
    send_list()


@app.route('/back_end_point')
@login_required
def admin():
    return render_template('admin.html')


@app.route('/logout')
def logout():
    logout_user()
    return 'log out success!'


@socketio.on('get', namespace='/manage')
def connect():
    send_list()


@socketio.on('connect', namespace='/manage')
def check_connect():
    if current_user.is_authenticated:
        pass
    else:
        return False


@socketio.on('archive', namespace='/manage')
def archive():
    ticket = Ticket.query.all()
    for t in ticket:
        t.status = 99
        db.session.add(t)
    db.session.commit()


@socketio.on('addEvent', namespace='/manage')
def addEvent(event):
    for i in Event.query.all():
        i.active = False
    e = Event()
    e.location = event['location']
    e.time = event['time']
    db.session.add(e)
    db.session.commit()


@socketio.on('startEvent', namespace='/manage')
def startEvent():
    e = Event.query.filter_by(active=True).first()
    e.running = 1
    db.session.add(e)
    db.session.commit()


@socketio.on('stopEvent', namespace='/manage')
def stopEvent():
    e = Event.query.filter_by(active=True).first()
    e.running = 2
    db.session.add(e)
    db.session.commit()


def send_list():
    data = {
        'waiting': [],
        'queuing': [],
        'repairing': [],
        'finished': [],
        'sent': [],
        'problem': [],
        'events': []
    }
    keys = ['waiting', 'queuing', 'repairing', 'finished', 'sent', 'problem']
    for j in range(0, 6):
        foo = Ticket.query.filter_by(status=j).order_by(Ticket.time).all()
        for i in foo:
            data[keys[j]].append({
                'short': i.short,
                'time': datetime.datetime.fromtimestamp(i.time).strftime("%Y-%m-%d %H:%M:%S"),
                'name': i.name,
                'tel': i.tel,
                'method': i.method,
                'model': i.model,
                'other': i.other,
            })
    for e in Event.query.all():
        desp = e.time + " " + e.location
        if e.active:
            desp = '*' + desp
        if e.running == 1:
            desp += ' - 活动中'
        elif e.running == 0:
            desp += ' - 预约中'
        else:
            desp += ' - 已结束'
        data['events'].append(desp)
    socketio.emit('list', data, namespace='/manage')


@app.route('/<int:id>')
def check(id):
    ticket = Ticket.query.filter_by(short=id).first()
    if ticket is not None:
        return render_template('track.html', status=ticket.status, message="工单号： %d" % id)
    else:
        # Protect brute-force attack to get ticket number
        return render_template('track.html', status=id % 6, message="工单号： %d" % id)


@app.route('/check')
def check_user():
    if current_user.is_authenticated:
        return "success!"
    else:
        return "unauthenticated!", 403


if __name__ == '__main__':
    # app.run()
    login_manager.login_view = 'login'
    socketio.run(app, debug=True, host='0.0.0.0')
