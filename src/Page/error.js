import React from 'react';
import {Link} from 'react-router-dom';
import PageTitle from '../Component/page-title.js';


class Error extends React.Component{
    constructor(props){
        super(props);
    }
    render(){
        return(
            <div id="page-wrapper">
                <PageTitle title="Error"/>
                <div className="row">
                    <div className="col-md-12">
                        <span>Still developing! </span>
                        <Link to = "/">back to home</Link>
                    </div>
                </div>
            </div>
        );
    }
}

export default Error;
