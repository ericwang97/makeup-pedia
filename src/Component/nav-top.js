import React  from 'react';
import {Link} from 'react-router-dom';
import './theme.css';

class NavTop extends React.Component{
    constructor(props){
        super(props);
    }

    onLogout(){
        alert("We don't need to log out hahahaha");
    }
    render(){
        return(
            <div className="navbar navbar-default top-navbar">
                <div className="navbar-header">
                    <Link className="navbar-brand" to="/"><b>My</b>News</Link>
                </div>

                <ul className="nav navbar-top-links navbar-left">
                    <li className="nav-item">
                        <Link className="top-navbar active"to="/"><b>Home</b></Link>
                    </li>
                    <li className="nav-item">
                        <Link className="top-navbar" to="/features"><b>Features Description</b></Link>
                    </li>
                    <li className="nav-item">
                        <Link className="top-navbar" to="/rate"><b>Rate it</b></Link>
                    </li>
                    <li className="nav-item">
                        <Link className="top-navbar" to="/rating-rating"><b>See my Rate!</b></Link>
                    </li>
                    <li className="nav-item">
                        <Link className="top-navbar disabled">To be continued</Link>
                    </li>
                </ul>


                <ul className="nav navbar-top-links navbar-right">
                    <li className="dropdown">
                        <a className="dropdown-toggle" href="javascript:;" >
                            <i className="fa fa-user fa-fw"/>
                            <span>Welcome!</span>
                            <i className="fa fa-caret-down"/>
                        </a>
                        <ul className="dropdown-menu dropdown-user">
                            <li>
                                <a onClick = {() => {this.onLogout()}}>
                                    <i className="fa fa-sign-out fa-fw"/>
                                    <span>Logout</span>
                                </a>
                            </li>
                        </ul>
                    </li>
                </ul>
            </div>
        );
    }
}


export default NavTop;
