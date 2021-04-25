import React from 'react';
import PageTitle from '../Component/page-title.js';
import './home.css'
import { Card } from "antd";
import 'antd/es/card/style/css'; // 加载 CSS

class Home extends React.Component{


    render(){
        return(
            <div id="page-wrapper">
                <PageTitle title="New's Data Integration System"/>
                <div className="row">
                    <Card title="Greeting" >
                    <div className="col-md-12">
                        <h5>Hey! Greeting from Liwei Wang!</h5>
                        <h5>This is my first full stack application, <b>individually</b>. Thank you for trying this!</h5>
                        <div>&nbsp;&nbsp;</div>
                        <h5>This is a <b>integrated information System</b>. See <b>Features Description</b> to find more details!</h5>
                        <div>&nbsp;&nbsp;</div>
                    </div>
                    </Card>
                    <div>&nbsp;&nbsp;</div>
                    <div>&nbsp;&nbsp;</div>
                    <Card title="Pipeline and Technology Stack" >
                        <div className="col-md-12">
                            <h5><b>Backend: </b> Python + Flask REST API + MySQL + Firebase</h5>
                            <h5><b>Front-end: </b> REACT.JS + ANT Design components</h5>
                            <h5><b>News Crawler: </b> Docker + Scrapy/Splash</h5>
                            <h5><b>NLP Processing and Analysis: </b> Text Similarity, TextRank, Stop Words Filtering, Synonym Detection, NLTK</h5>
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
