import React, {Component} from 'react';

import {Segment, Label, Grid, Card, Button, Transition, Modal, Header, Form, TextArea} from 'semantic-ui-react';
import SnackBar from './SnackBar';
const colors = [
    "red",
    "orange",
    "yellow"
];

class Tab extends Component{

    componentWillMount(){
        this.setState({message: false, hint: '请求已发送', problem: false, id: 0});
    }
    handleCloseMessage = () => {this.setState({message: false})};
    handleRequest = (type, id) => {
        if(type === 'problem'){
            this.setState({problem: true, id: id});
            return ;
        }
        this.props.socket.emit(type, {id: id});
        this.setState({message: true, hint: '请求已发送'});
    };
    actions = (section, id) => {
        let action = [];
        switch (section){
            case "waiting":
                action = [
                    ['green', 'receive', 'Approve'],
                    ['red', 'reject', 'Decline']
                ];
                break;
            case "queuing":
                action = [
                    ['green', 'start', 'Start']
                ];
                break;
            case "repairing":
                action = [
                    ['yellow', 'problem', 'Question'],
                    ['green', 'finish', 'Finish'],
                ];
                break;
            case "finished":
                action = [
                    ['green', 'sent', 'Claim']
                ];
                break;
            case "problem":
                action = [
                    ['orange', 'start', 'Fixed']
                ];
                break;
            default:
                return ('')
        }

        return (
                    <div className={`ui ${action.length === 1 ? 'one': (action.length === 2 ? 'two' : 'three')} buttons`} >
                        {action.map(item=>(
                            <Button basic color={item[0]} onClick={() => this.handleRequest(item[1], id)}>
                                {item[2]}
                            </Button>
                        ))}
                    </div>
        );
};
    render() {
        const {nodes} = this.props;
        const {message, hint, problem} = this.state;
        let i = 0;
        return (
            <div style={{position: 'relative', left: '5%', width: '90vw'}}>
                <Modal open={problem}>
                    <Header> What's Wrong? </Header>
                    <Modal.Content>
                        <Form>
                            <TextArea placeholder="Notify the owner and get response" onChange={(e,d)=>{this.setState({value: d.value})}}/>
                        </Form>
                    </Modal.Content>
                    <Modal.Actions>
                        <Button color='red' onClick={()=>{this.setState({problem: false})}}>No problem</Button>
                        <Button color='green' onClick={()=>{this.props.socket.emit('problem', {id: this.state.id, problem: this.state.value});this.setState({problem: false, message: true})}}>Send</Button>
                    </Modal.Actions>
                </Modal>
                <SnackBar message={message} content={hint} onClose={this.handleCloseMessage.bind(this)}/>
                    {nodes.map((item)=>(
                        <div key={i}>
                            <div style={{display: 'none'}}>{i++}</div>
                            <Segment color={colors[i-1]} raised>
                                <Label attached="top left" ribbon color={colors[i-1]}>{item[0]} </Label>
                                <Transition.Group fluid as={Card} duration={1000} size='huge' animation="browse">
                                {item[1].map((record)=>(
                                    <Card fluid>
                                        <Card.Content header={`Ticket: ${record['short']}`}/>
                                        <Card.Content description>
                                            <Grid celled>
                                                <Grid.Row>
                                                    <Grid.Column width={5}>
                                                        {record['name']}
                                                    </Grid.Column>
                                                    <Grid.Column width={11}>
                                                        {record['model']}
                                                    </Grid.Column>
                                                </Grid.Row>
                                                <Grid.Row>
                                                    <Grid.Column width={5}>
                                                        手机
                                                    </Grid.Column>
                                                    <Grid.Column width={11}>
                                                        {record['tel']}
                                                    </Grid.Column>
                                                </Grid.Row>
                                                <Grid.Row>
                                                    <Grid.Column width={5}>
                                                        项目
                                                    </Grid.Column>
                                                    <Grid.Column width={11}>
                                                        {record['method']}
                                                    </Grid.Column>
                                                </Grid.Row>
                                                {record['other'].length ? <Grid.Row><Grid.Column>{`补充：${record['other']}`}</Grid.Column></Grid.Row> : ''}
                                            </Grid>
                                        </Card.Content>
                                        <Card.Content extra>
                                            {this.actions(item[0], record['short'])}
                                            <div className="right aligned">{record['time']}</div>
                                        </Card.Content>
                                    </Card>
                                    )

                                )}
                                </Transition.Group>
                                {item[1].length ? '' : <Card fluid>
                                    <Card.Content extra>
                                        No Ticket
                                    </Card.Content>
                                </Card>}
                                </Segment>
                        </div>
                ))}
                <div style={{height: '3em', color: 'gray', paddingBottom: '10em'}}><p/><p/> All Right Reserved by @HUSTCA</div>
            </div>
        )
    }
}

export default Tab;