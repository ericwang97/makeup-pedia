import React from 'react';
import PageTitle from '../Component/page-title.js';
import './home.css'
import { Card } from "antd";
import 'antd/es/card/style/css'; // 加载 CSS

class Home extends React.Component{


    render(){
        return(
            <div id="page-wrapper">
                <PageTitle title="MAKEUP PEDIA"/>
                <div className="row">
                    <Card title="Greeting" >
                    <div className="col-md-12">
                        <h5>Hey! Greeting from Liwei Wang and Jiaying Wang!</h5>
                        <h5>Thank you for trying this wonderful Makeup-Pedia!</h5>
                        <div>&nbsp;&nbsp;</div>
                        <h5>This is an <b>integrated make-up products websites based on Knowledge Graph</b>. See <b>Features Description</b> to find more details!</h5>
                        <div>&nbsp;&nbsp;</div>
                    </div>
                    </Card>
                    <div>&nbsp;&nbsp;</div>
                    <div><img src="https://www.beautypedia.com/wp-content/uploads/2018/08/bp-home-header.jpg"/></div>
                    <div>&nbsp;&nbsp;</div>
                    <Card title="Pipeline and Technology Stack" >
                        <div className="col-md-12">
                            <h5><b>Backend: </b> Python + Flask REST API + Neo4J, Py2Neo</h5>
                            <h5><b>Front-end: </b> REACT.JS + ANT Design components</h5>
                            <h5><b>Products Crawler: </b> Docker + Scrapy/Splash + Selenium</h5>
                            <h5><b>Entity Resolution: </b> String Similarity, NLTK</h5>
                            <h5><b>Recommendation: </b> User-Based Collaborative Filtering, Embedding</h5>
                            <h5><b>Server and Deployment: </b> Amazon Web Server EC2, Multiprocessing, Scheduler</h5>
                            <div>&nbsp;&nbsp;</div>
                            <h5>So hard to make a full stack application, thank you for the people who helped and supported me.</h5>
                        </div>
                    </Card>

                </div>
            </div>


        );
    }
}

export default Home;
