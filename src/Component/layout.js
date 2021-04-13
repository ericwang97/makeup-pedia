import React from 'react';

import NavTop from './nav-top.js';
import NavSide from './nav-side-2.js';
import './theme.css';

class Layout extends React.Component{
    constructor(props){
        super(props);
    }

    render(){
        return(
            <div id="wrapper">
                <NavTop/>
                <NavSide/>
                {this.props.children}
            </div>
        );
    }
}


export default Layout;
