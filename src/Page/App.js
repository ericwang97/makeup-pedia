import React from 'react';
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

class App extends React.Component {


    constructor(props) {
        super(props);

        this.state = {
            database: null,
            table: "",
            searchwords: null,
            searchNews: null,
            loading: true,
            queryData: null,
            queryDataKey: null,
            recommendation: "",
            clickPK: false,
            history: []
        };
        this.handleSearchClick = this.handleSearchClick.bind(this);
        this.handleDatabaseChange = this.handleDatabaseChange.bind(this);
        this.handleTableChange = this.handleTableChange.bind(this);
        this.handleSearchwordsChange = this.handleSearchwordsChange.bind(this);
        this.handleSearchNewsChange = this.handleSearchNewsChange.bind(this);
        this.handleResetClick = this.handleResetClick.bind(this);
        this.handleGoBackClick = this.handleGoBackClick.bind(this);
        this.handleHyperLinkClick = this.handleHyperLinkClick.bind(this);
    }

    handleSearchClick() {
        let currentComponent = this;
        if (currentComponent.state.clickPK === false) {
            let url = "http://13.57.28.139:8000/search?databasename=" + currentComponent.state.database +
                "&tablelist=" + currentComponent.state.table +
                "&searchwords=" + currentComponent.state.searchwords;
            let firebaseurl = "https://inf551-a79f9.firebaseio.com/" + currentComponent.state.database + "Node/" +
                ".json?orderBy=\"$key\"&limitToFirst=1";

            axios.get(firebaseurl).then(function (response) {
                let data = response.data;
                if (data === null)
                    alert("Index file doesn't exist, Initializing will take a while..");
            });

            axios.get(url)
                .then(function (response) {
                    let data = response.data.data;
                    let status = response.data.status;
                    let dataKey = response.data.tableKey;
                    let recommendation = response.data.Recommendation;

                    if (status === 0) {
                        currentComponent.setState({
                            loading: false, queryDataKey: dataKey,
                            recommendation: recommendation, queryData: data
                        });

                        let history = currentComponent.state.history;
                        history.push(currentComponent.state)
                        currentComponent.setState({history:history})

                    } else {
                        alert(response.data.msg);
                    }
                })
                .catch(function (error) {
                    alert("error");
                    console.log(error);

                });
        } else {
            let url = "http://13.57.28.139:8000/query?databasename=" + currentComponent.state.database +
                "&tablelist=" + currentComponent.state.table +
                "&value=" + currentComponent.state.searchwords;

            axios.get(url)
                .then(function (response) {
                    let data = response.data;
                    let status = response.data.status;

                    //console.log(data);
                    if (status === 0) {
                        currentComponent.setState({loading: false, queryData: data});

                        let history = currentComponent.state.history;
                        history.push(currentComponent.state)
                        currentComponent.setState({history:history})

                    } else {
                        alert(response.data.msg);
                    }
                })
                .catch(function (error) {
                    alert("error");
                    console.log(error);

                });
        }
    }

    handleResetClick() {
        this.setState({
            database: "",
            table: "",
            searchwords: "",
            loading: true,
            queryData: null,
            queryDataKey: null,
            recommendation: "",
            clickPK: false,
            history: []
        })
    }

    handleGoBackClick() {
        let currentComponent = this;
        //window.location.reload();
        //console.log(this.props.history.goBack);
        //console.log(window.history.back());

        let historyList = currentComponent.state.history;

        if(historyList.length >1) {
            let history = historyList[historyList.length-2];
            this.setState(history);
            historyList.pop();
        }
        else{
            alert("Can't go back any more!");
        }

    }

    handleHyperLinkClick(table,searchwords) {
        let currentComponent = this;
        currentComponent.setState({
                table: table,
                loading: true,
                clickPK: true,
                searchwords: searchwords},
            this.handleSearchClick);
    }

    handleSearchNewsChange(value) {
        this.setState({searchNews: value,loading:true, database: null, table: null});
    }

    handleDatabaseChange(value) {
        this.setState({database: value,loading:true, table: null});
    }

    handleTableChange(value) {
        this.setState({table:value,loading:true});
    }

    handleSearchwordsChange(event) {
        this.setState({searchwords: event.target.value,loading:true});
    }

    render() {

        let selectDatabase = [];
        if (this.state.searchNews === null) {
            selectDatabase.push(
                <Select/>
            );
        }
        else if (this.state.searchNews === 'news') {
            this.state.database = 'news'
            selectDatabase.push(
                <Select/>
                // <Select
                //     style={{ width: 160 }}
                //     placeholder="Select a person"
                //     onChange={this.handleDatabaseChange}
                //     value={this.state.database}>
                //     <Option value="news">News</Option>
                // </Select >
            );
        }
        else {
            selectDatabase.push(
                    <Select
                        defaultValue="world"
                        style={{ width: 160 }}
                        placeholder="Select a person"
                        onChange={this.handleDatabaseChange}
                        value={this.state.database}>
                        <Option value="world">World</Option>
                        <Option value="sakila">Film Dataset</Option>
                        <Option value="customers_order">Customers Order</Option>
                    </Select >
                );
            }

        let selectTable = [];
        if (this.state.database === null) {
            selectTable.push(
                <Select/>
            );
        }
        else if (this.state.database === "news") {
            selectTable.push(
                <Select
                    name="table"
                    defaultValue=""
                    style={{ width: 160 }}
                    onChange={this.handleTableChange}
                    value={this.state.table}>
                    <Option value="tweet">Tweet</Option>
                    <Option value="tweet">Financial Times (TBD)</Option>
                    <Option value="">All tables</Option>
                </Select>
            );
        }
        else if (this.state.database === "world") {
            selectTable.push(
                <Select
                    name="table"
                    defaultValue=""
                    style={{ width: 160 }}
                    onChange={this.handleTableChange}
                    value={this.state.table}>
                    <Option value="city">city</Option>
                    <Option value="country">country</Option>
                    <Option value="countrylanguage">country language</Option>
                    <Option value="">All tables</Option>
                </Select>
            );
        }
        else if (this.state.database === "customers_order") {
            selectTable.push(
                <Select
                    name="table"
                    defaultValue=""
                    style={{ width: 160 }}
                    onChange={this.handleTableChange}
                    value={this.state.table}>
                    <Option value="customers">customers</Option>
                    <Option value="employees">employees</Option>
                    <Option value="offices">offices</Option>
                    <Option value="orderdetails">order details</Option>
                    <Option value="orders">orders</Option>
                    <Option value="payments">payments</Option>
                    <Option value="productlines">product lines</Option>
                    <Option value="products">products</Option>
                    <Option value="">All tables</Option>
                </Select>
            );
        }
        else if (this.state.database === "sakila") {
            selectTable.push(
                <Select
                    name="table"
                    defaultValue=""
                    style={{ width: 160 }}
                    onChange={this.handleTableChange}
                    value={this.state.table}>
                    <Option value="actor">actor</Option>
                    <Option value="address">address</Option>
                    <Option value="category">category</Option>
                    <Option value="city">city</Option>
                    <Option value="country">country</Option>
                    <Option value="customer">customer</Option>
                    <Option value="film">film</Option>
                    <Option value="film_actor">film actor</Option>
                    <Option value="film_category">film category</Option>
                    <Option value="film_text">film text</Option>
                    <Option value="inventory">inventory</Option>
                    <Option value="language">language</Option>
                    <Option value="payment">payment</Option>
                    <Option value="rental">rental</Option>
                    <Option value="staff">staff</Option>
                    <Option value="store">store</Option>
                    <Option value="">All tables</Option>
                </Select>
            );
        }


        let returnResult = [];
        if (this.state.loading === true) {
            if (this.state.clickPK === false) {
                returnResult.push(<div>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</div>)
                returnResult.push(<div style={{"fontSize": "15px"}}>Please enter your search
                    words... &nbsp;(*╹▽╹*)&nbsp;</div>);
            } else {
                let columnName = this.state.database + "_" + this.state.table;
                returnResult.push(<div>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</div>)
                returnResult.push(<div style={{"fontSize": "15px"}}>loading... &nbsp;(*╹▽╹*)&nbsp;</div>)
                returnResult.push(<div>&nbsp;&nbsp;</div>);
                returnResult.push(
                    <TableList
                               columnName={columnName}
                               dataSource={null}
                               loading={this.state.loading}
                               handleHyperLinkClick = {this.handleHyperLinkClick}/>
                );
            }
        }
        else {
            returnResult.push(<div>&nbsp;&nbsp;</div>);
            if (this.state.clickPK === false) {
                returnResult.push(<div style={{"font-size": "15px"}}>Searching results
                    of: {this.state.searchwords} </div>);
                returnResult.push(<div style={{"font-size": "15px"}}>Most relevant
                    table:&nbsp; {this.state.recommendation} &nbsp;&nbsp;</div>);
            } else {
                returnResult.push(<div style={{"font-size": "15px"}}>Redirect to: {this.state.searchwords} </div>);
            }
            //returnResult.push(<div style={{"font-size":"15px"}}>Click PK:&nbsp; {this.state.clickPK} &nbsp;&nbsp;</div>);
            returnResult.push(<div>&nbsp;&nbsp;</div>);

            if (this.state.clickPK === true) {

                let columnName = this.state.database + "_" + this.state.table;
                returnResult.push(<TableList tableName={this.state.table}
                                             columnName={columnName}
                                             dataSource={this.state.queryData.data}
                                             handleHyperLinkClick = {this.handleHyperLinkClick}/>)
            }
            else {
                if (this.state.recommendation !== "No recommended tables") {
                    let recommendColumnName = this.state.database + "_" + this.state.recommendation;
                    let recommedPK = this.state.queryDataKey[this.state.recommendation];

                    returnResult.push(<TableList tableName={this.state.recommendation}
                                                 columnName={recommendColumnName}
                                                 dataSource={this.state.queryData[this.state.recommendation][recommedPK]}
                                                 handleHyperLinkClick = {this.handleHyperLinkClick}/>);
                }
                for (let table in this.state.queryData) {
                    let columnName = this.state.database + "_" + table;
                    let PK = this.state.queryDataKey[table];
                    if (table !== this.state.recommendation) {
                        returnResult.push(<TableList tableName={table}
                                                     columnName={columnName}
                                                     dataSource={this.state.queryData[table][PK]}
                                                     handleHyperLinkClick = {this.handleHyperLinkClick}/>);
                    }
                }
            }
            //if (data.hasOwnProperty("countrylanguage"))
        }

        return (

            <div id="page-wrapper">
                <div className="App-header">
                    {/*<img src={logo} className="App-logo" alt="logo"/>*/}
                    <h1>Search Engine </h1>

                </div>
                <div className="App-search">

                    <label htmlFor="ifNews">
                        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Search News? &nbsp;&nbsp;
                        <Select
                            defaultValue="news"
                            style={{ width: 160 }}
                            placeholder="Select a person"
                            onChange={this.handleSearchNewsChange}
                            value={this.state.searchNews}>
                            <Option value="news">Yes, search news</Option>
                            <Option value="database">No, search database</Option>

                        </Select >
                    </label>

                    <label htmlFor="database">
                        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Database: &nbsp;&nbsp;
                        {selectDatabase}
                    </label>

                    <label htmlFor="table">
                        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Table: &nbsp;&nbsp;
                        {selectTable}
                    </label>

                    <label htmlFor="searchwords">
                        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                        <Input
                            id="searchwords"
                            style={{ width: 300 }}
                            placeholder="Search words or a whole sentence"
                            onChange={this.handleSearchwordsChange}
                            value={this.state.searchwords}
                        />
                    </label>


                </div>
                <div className="App-header">
                    <div>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</div>
                    <div>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</div>
                    <div>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</div>
                    <div>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</div>
                    <div>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</div>

                    <Button onClick={(e) => this.handleGoBackClick()}
                    >Go Back</Button>
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    <Button type="primary" icon={<SearchOutlined />}
                            onClick= {this.handleSearchClick}
                    >Search</Button>
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

export default App;
