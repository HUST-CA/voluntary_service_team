import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import {Modal, Button, Menu, Dropdown, Icon, Header, Transition, Rail, Sticky, Input} from 'semantic-ui-react';
import SnackBar from './SnackBar';
import Tab from './Tab';

const socket = global.io.connect('https://nservice.hustca.com/manage');
// const socket = global.io.connect('http://localhost:5000/manage');
const login = new XMLHttpRequest();
const TabStyle = {position: 'fixed',
    overflowY: 'scroll',
    overflowX: 'hidden',
    width:'100vw',
    height:'95vh',
    WebkitOverflowScrolling: 'touch',
};
login.onreadystatechange = () => {
    if (login.readyState == 4 && login.status == 403) {
        window.location = '/login';
    }
};
login.open('GET', '/check', true);

login.send();
class App extends Component {
    componentWillMount(){
        this.setState({archive: false, message: false, hint: '归档成功！', active: 1, pending: [], finished: [], waiting: [], events:[]});
        socket.on('list', this.handleList.bind(this));
        if (!socket.connected) {
            socket.on('connect', ()=> {socket.emit('get')})
        }
        socket.emit('get');

    }
    componentDidMount(){
        if (socket.connected) {

        }
    }
    handleList(data){
        this.setState({
            pending:
                [['waiting', data['waiting']], ['queuing', data['queuing']]],
            finished:
                [['finished', data['finished']], ['sent', data['sent']]],
            waiting:
                [['repairing', data['repairing']], ['problem', data['problem']]],
            events:
                data['events']
        });
    }
  render() {
      const {archive, message, hint,active, pending, finished, waiting, addEvent, events} = this.state;
    return (
      <div className="App">
            <SnackBar message={message} content={hint} onClose={()=>{this.setState({message: false})}} />
          <Sticky>
          <Menu attached="top" pointing>
              <Dropdown icon="wrench" item simple>
                  <Dropdown.Menu>
                      <Dropdown.Item>
                          <Icon name='dropdown' />
                          <span className='text'>数据归档</span>
                          <Dropdown.Menu>
                              <Modal trigger={<Dropdown.Item onClick={()=>{this.setState({archive: true})}}>全部归档</Dropdown.Item>} open={archive} basic size='small'>
                                  <Header icon='archive' content='确认进行数据归档？' />
                                  <Modal.Content>
                                      <p>
                                          归档将隐藏当前全部维修记录
                                      </p>
                                  </Modal.Content>
                                  <Modal.Actions>
                                      <Button basic color='red' inverted onClick={()=>{this.setState({archive: false})}}>
                                          <Icon name='remove' /> 取消
                                      </Button>
                                      <Button color='green' inverted onClick={()=>{socket.emit('archive');socket.emit('get');this.setState({archive: false, message: true});}}>
                                          <Icon name='checkmark' /> 确认
                                      </Button>
                                  </Modal.Actions>
                              </Modal>
                              <Dropdown.Item disabled>查看归档（开发中）</Dropdown.Item>
                          </Dropdown.Menu>
                      </Dropdown.Item>
                      <Dropdown.Item>
                          <Icon name='dropdown' />
                          <span className='text'>活动管理</span>
                          <Dropdown.Menu>
                              <Dropdown.Item>
                                  <Dropdown icon='dropdown' simple text={"全部活动"}>
                                  <Dropdown.Menu>
                                      {events.map((item) => (
                                          <Dropdown.Item>
                                              <span className='text'>{item}</span>
                                          </Dropdown.Item>
                                      ))}

                                  </Dropdown.Menu>
                                  </Dropdown>
                              </Dropdown.Item>
                              <Modal trigger={<Dropdown.Item onClick={()=>{this.setState({addEvent: true})}}>添加新活动</Dropdown.Item>} open={addEvent} basic size='small'>
                                  <Header icon='add' content='请输入活动信息' />
                                  <Modal.Content>
                                      <div style={{ width: '100%'}}>
                                          <p>
                                              <Input placeholder={'活动地点'} style={{width: '100%'}} onChange={(e)=>{this.setState({eventLocation: e.target.value})}}/>
                                          </p>

                                          <p>
                                              <Input placeholder={'活动时间'} style={{width: '100%'}} onChange={(e)=>{this.setState({eventTime: e.target.value})}}/>
                                          </p>
                                      </div>

                                  </Modal.Content>
                                  <Modal.Actions>
                                      <Button basic color='red' inverted onClick={()=>{this.setState({addEvent: false})}}>
                                          <Icon name='remove' /> 取消
                                      </Button>
                                      <Button color='green' inverted onClick={()=>{socket.emit('addEvent', {location: this.state.eventLocation,time: this.state.eventTime});socket.emit('get');this.setState({hint: '请求已发送', addEvent: false, message: true});}}>
                                          <Icon name='checkmark' /> 确认
                                      </Button>
                                  </Modal.Actions>
                              </Modal>
                              <Dropdown.Item onClick={()=>{socket.emit('startEvent');socket.emit('get'); this.setState({hint: '请求已发送', message: true}); }}>开始当前活动</Dropdown.Item>
                              <Dropdown.Item onClick={()=>{socket.emit('stopEvent');socket.emit('get'); this.setState({hint: '请求已发送', message: true});}}>结束当前活动</Dropdown.Item>
                              {/*<Dropdown.Item disabled>查看归档（开发中）</Dropdown.Item>*/}
                              {/*<Dropdown.Item disabled>查看归档（开发中）</Dropdown.Item>*/}
                              {/*<Dropdown.Item disabled>查看归档（开发中）</Dropdown.Item>*/}
                              {/*<Dropdown.Item disabled>查看归档（开发中）</Dropdown.Item>*/}
                          </Dropdown.Menu>
                      </Dropdown.Item>
                  </Dropdown.Menu>
              </Dropdown>
              <Menu.Item active={active === 1} onClick={()=>{this.setState({active: 1})}}>Pending</Menu.Item>
              <Menu.Item active={active === 2} onClick={()=>{this.setState({active: 2})}}>Waiting</Menu.Item>
              <Menu.Item active={active === 3} onClick={()=>{this.setState({active: 3})}}>Finished</Menu.Item>
          </Menu>
          </Sticky>
          <div style={{position: 'relative'}}>
              <Transition visible={active === 1} animation={'fade right'} duration={500} >
                  <div style={TabStyle}> <Tab nodes={pending} socket={socket}></Tab></div>
              </Transition>
              <Transition visible={active === 2} animation={active === 1  ? active === 3 ? 'fade left' : 'fade right' : 'fade up'} duration={500} >
                  <div style={TabStyle}> <Tab nodes={waiting} socket={socket}/> </div>
              </Transition>
              <Transition visible={active === 3} animation='fade left' duration={500} >
                  <div style={TabStyle}> <Tab nodes={finished} socket={socket}/>    </div>
              </Transition>
          </div>
      </div>
    );
  }
}

export default App;
