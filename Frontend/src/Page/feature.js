import React from 'react';
import PageTitle from '../Component/page-title.js';
import './home.css'
import { Card } from "antd";
import 'antd/es/card/style/css'; // 加载 CSS

class Feature extends React.Component{


    render(){
        return(
            <div id="page-wrapper">
                <PageTitle title="Description of Features"/>
                <div className="row">
                    <Card title="1. Search Engine" >
                        <div className="col-md-12">
                            <h5>Search Engine is based on <b>inverted index and word frequency</b>, you could input whatever sentences or phrase you like. </h5>
                            <div>&nbsp;&nbsp;</div>
                        </div>
                    </Card>
                    <div>&nbsp;&nbsp;</div>
                    <Card title="2. New's Crawler" >
                        <div className="col-md-12">
                            <h5>1. Enable to run daily news crawler by using <b>scheduler</b></h5>
                            <h5>2. Use <b>Run Crawler</b> Page to select your <b>personal interested topic and websites</b>. Try getting your own news!</h5>
                            <div>&nbsp;&nbsp;</div>
                        </div>
                    </Card>
                    <div>&nbsp;&nbsp;</div>
                    <Card title="3. NLP Processing, Analysis, and Recommendation" >
                        <div className="col-md-12">
                            <h5>1. Do you like this news? Select which one you like, click them and help me to find and <b>recommend</b> the better news on next crawler!!</h5>
                            <h5>2. Don't satisfied with the search results? Try using <b>Stop Words filtering</b>, <b>Synonym filtering</b> to improve the results!</h5>
                            <h5>3. Try using <b>Text-Rank</b> to generate the keywords and abstracts for crawled articles!</h5>
                            <h5>4. Try implementing <b>Word Cloud</b></h5>
                            <div>&nbsp;&nbsp;</div>
                        </div>
                    </Card>
                    <div>&nbsp;&nbsp;</div>
                    <Card title="4. Database Presentation" >
                        <div className="col-md-12">
                            <h5>Used three databases: World, Film, Customers_Orders as the examples to show the presentation of database, and allow the users to <b>navigate the FK relationships</b> of tables. </h5>
                            <h5>You can click the DB example and select the table to take a look at the data</h5>
                            <div>&nbsp;&nbsp;</div>
                        </div>
                    </Card>

                </div>
            </div>


        );
    }
}

export default Feature;
