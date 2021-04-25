import React from 'react';
import PageTitle from '../Component/page-title.js';
import './home.css'
import { Card } from "antd";
import 'antd/es/card/style/css';

class Search extends React.Component{


    render(){
        return(
            <div id="page-wrapper">
                <PageTitle title="Neo4J"/>
                <div className="row">
                    <Card title="Analysis the article and Visualize it" >
                        <div className="col-md-12">
                            <h5>Analysis the article and Visualize it</h5>
                            <div>Analysis the article and Visualize it.</div>
                        </div>
                    </Card>

                </div>
            </div>


        );
    }
}

export default Search;
