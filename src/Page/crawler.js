import React from 'react';
import PageTitle from '../Component/page-title.js';
import './home.css'
import 'antd/es/card/style/css'; // 加载 CSS

import logo from '../logo.svg';
import './App.css';
import axios from 'axios' ;
import {Layout, Menu, Pagination, Skeleton, Divider, Table, Select ,Button,Input , Card} from 'antd';
import 'antd/es/input/style/css'; // 加载 CSS
import { SearchOutlined } from '@ant-design/icons';
import TableList from '../tableList/tableList.js';

//const { Header, Content } = Layout;
//const { SubMenu } = Menu;
const { Search } = Input;
const { Option } = Select;

// import {BrowserRouter as Router, Switch, Route} from "react-router-dom";
// import {useHistory} from "react-router-dom";
// import { withRouter } from "react-router";
// import PropTypes from "prop-types";

class Crawler extends React.Component {


    constructor(props) {
        super(props);

        this.state = {
            web: null,
            topic: null,
            searchwords: null,
            loading: true,
            queryData: null,
        };
        this.handleSearchClick = this.handleSearchClick.bind(this);
        this.handleWebChange = this.handleWebChange.bind(this);
        this.handleTopicChange = this.handleTopicChange.bind(this);
        this.handleSearchwordsChange = this.handleSearchwordsChange.bind(this);
        this.handleResetClick = this.handleResetClick.bind(this);
    }

    handleSearchClick() {
        let currentComponent = this;

        alert("TBD")
        console.log(this.state.web)
        console.log(this.state.topic)


    }

    handleResetClick() {
        this.setState({
            web: null,
            topic: null,
            searchwords: null,
            loading: true,
            queryData: null,
        })
    }


    handleWebChange(value) {
        this.setState({web:value,loading:true});
    }

    handleTopicChange(value) {
        this.setState({topic:value,loading:true});
    }

    handleSearchwordsChange(event) {
        this.setState({searchwords: event.target.value,loading:true});
    }

    render() {


        let returnResult = [];
        if (this.state.loading === true) {
            returnResult.push(<div>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</div>)
            returnResult.push(<div style={{"fontSize": "15px"}}>Run the Crawler to get your own topic of news... &nbsp;(*╹▽╹*)&nbsp;</div>);
        }
        else {
            returnResult.push(<div>TBD</div>);

        }

        return (

            <div id="page-wrapper">
                <div className="App-header">
                    {/*<img src={logo} className="App-logo" alt="logo"/>*/}
                    <h1>Run Crawler </h1>

                </div>
                <div className="App-search">


                    <label htmlFor="table">
                        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Select News Web: &nbsp;&nbsp;
                        <Select
                            name="table"
                            defaultValue=""
                            style={{ width: 160 }}
                            onChange={this.handleWebChange}
                            value={this.state.web}>
                            <Option value="tweet">Tweet</Option>
                            <Option value="FT">Financial Times (TBD)</Option>
                            <Option value="">All Webs</Option>
                        </Select>
                    </label>

                    <label htmlFor="topic">
                        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Select News Topic: &nbsp;&nbsp;
                        <Select
                            name="topic"
                            defaultValue=""
                            style={{ width: 160 }}
                            onChange={this.handleTopicChange}
                            value={this.state.topic}>
                            <Option value="music">Music</Option>
                            <Option value="other">Other</Option>
                            <Option value="">All Topic</Option>
                        </Select>
                    </label>


                </div>
                <div className="App-header">
                    <div>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</div>
                    <div>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</div>
                    <div>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</div>
                    <div>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</div>

                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    <Button type="primary" icon={<SearchOutlined />}
                            onClick= {this.handleSearchClick}
                    >Run Crawler</Button>
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    <Button onClick=
                                {this.handleResetClick}
                    >Reset</Button>
                    <Divider/>
                </div>
                <div className="App-body">
                    <div style={{"fontSize": "13px"}}>{returnResult}</div>
                </div>
            </div>

        );
    }
}

export default Crawler;
