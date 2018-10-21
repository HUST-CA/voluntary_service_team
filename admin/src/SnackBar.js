import React ,{Component} from 'react';

import {Portal, Message} from 'semantic-ui-react';

class SnackBar extends Component{
    constructor(property){
        super(property);
    }
    componentWillMount(){
        this.setState({transparent: 1, trigger: false});
    }

    render() {
        const {message, content} = this.props;
        const {transparent, trigger} = this.state;
        if(!trigger && message) {
            setTimeout(()=>{
                this.setState({transparent: 0, trigger: false});
                setTimeout(()=>{
                    this.props.onClose();
                    this.setState({transparent: 1})
                }, 1000);
            }, 2000)
        }
        return (
        <Portal open={message}>
            <div onClick={this.props.onClose}>

            <Message success floating style={{ left: '50%', transform: 'translateX(-50%)', top: '50%', position: 'fixed', zIndex: '1000', opacity: transparent, WebkitTransition: 'opacity 1s ease-in-out',
                transition: 'opacity 1s ease-in-out'} }>{ content }
                </Message>

                <span style={{position: "fixed", height: '10000%', width: '10000%', backgroundColor:"#00000099", left:'-50vw', top:'-100vh', zIndex: '999', opacity: transparent, WebkitTransition: 'opacity 1s ease-in-out',
                    transition: 'opacity 1s ease-in-out'}}/>
            </div>
        </Portal>
        );
    }
}


export default SnackBar;