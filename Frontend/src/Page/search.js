import React from 'react';
import PageTitle from '../Component/page-title.js';

import './App.css';
import axios from 'axios' ;
import {Layout, Menu, Pagination, Skeleton, Divider, Table, Select, Button, Input, Card, Radio} from 'antd';
import 'antd/es/input/style/css';
import { SearchOutlined } from '@ant-design/icons';
import TableList from '../tableList/tableList.js';

// const { Search } = Input;
const { Option } = Select;
const options = [
    { label: 'Table Display', value: "false" },
    { label: 'Neo4J Visualization', value: "true" },
];


class Search extends React.Component{

    constructor(props) {
        super(props);

        this.state = {
            product_id: null,
            product_name: null,

            category: null,
            subcategory: null,
            search_name: null,

            loading: true,
            response_data: null,

            history: [],

            is_neo: "false"

        };
        this.handleResetClick = this.handleResetClick.bind(this);
        this.handleGoBackClick = this.handleGoBackClick.bind(this);
        this.handleSearchClick = this.handleSearchClick.bind(this);
        this.handleSearchSimilarClick = this.handleSearchSimilarClick.bind(this);
        this.handleAutoFillClick = this.handleAutoFillClick.bind(this);
        this.handleHyperLinkClick = this.handleHyperLinkClick.bind(this);

        this.handleCategoryChange = this.handleCategoryChange.bind(this);
        this.handleSubCategoryChange = this.handleSubCategoryChange.bind(this);
        this.handleSearchNameChange = this.handleSearchNameChange.bind(this);
        this.handleDisplayChange = this.handleDisplayChange.bind(this);
    }

    handleResetClick() {
        this.setState({
            product_id: null,
            product_name: null,
            category: null,
            subcategory: null,
            search_name: null,
            loading: true,
            response_data: null,
            history: [],
            is_neo: "false"
        })
    }

    handleGoBackClick() {
        let currentComponent = this;

        let historyList = currentComponent.state.history;

        if(historyList.length > 1) {
            let history = historyList[historyList.length - 2];
            this.setState(history);
            historyList.pop();
        }
        else{
            alert("Can't go back any more!");
        }

    }

    handleSearchClick() {
        let currentComponent = this;
        // let base_url = "http://13.57.28.139:8000/";
        let url = "http://localhost:8000/search";

        axios.post(url,{
            category: currentComponent.state.category,
            subcategory: currentComponent.state.subcategory,
            search_name: currentComponent.state.search_name
        })
            .then(function (response) {
                let status = response.data.status;
                if (status === 0) {
                    let response_data = response.data.response
                    currentComponent.setState({
                        loading: false, response_data: response_data
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

    }

    handleSearchSimilarClick() {
        let currentComponent = this;
        // let base_url = "http://13.57.28.139:8000/";
        let url = "http://localhost:8000/find_similar";
        axios.post(url,{
            product_id: currentComponent.state.product_id
        })
            .then(function (response) {
                let status = response.data.status;
                if (status === 0) {
                    let response_data = response.data.response
                    currentComponent.setState({
                        loading: false, response_data: response_data
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

    }

    handleAutoFillClick() {
        this.setState({
            category: "Face Makeup",
            subcategory: "Face Powder",
            search_name: "Pureness Matifying Compact Oil-Free SPF 16",
            loading: true,
            response_data: null
        })
    }

    handleHyperLinkClick(product_id, product_name) {
        let currentComponent = this;
        currentComponent.setState({
                loading: true,
                product_id: product_id,
                product_name: product_name
            },
            this.handleSearchSimilarClick);
    }

    handleCategoryChange(value) {
        this.setState({category: value, loading: true, subcategory: null});
    }

    handleSubCategoryChange(value) {
        this.setState({subcategory: value, loading: true});
    }

    handleSearchNameChange(event) {
        this.setState({search_name: event.target.value, loading: true});
    }

    handleDisplayChange(event) {
        this.setState({is_neo: event.target.value, loading: false});
    }


    render(){

        let select_subcategory = [];
        if (this.state.category === null) {
            select_subcategory.push(
                <Select/>
            );
        }
        else if (this.state.category === "Face Makeup") {
            select_subcategory.push(
                <Select
                    defaultValue="Face Powder"
                    style={{ width: 160 }}
                    placeholder="Select a Face Makeup!"
                    onChange={this.handleSubCategoryChange}
                    value={this.state.subcategory}>
                    <Option value="Cushion Foundation">Cushion Foundation</Option>
                    <Option value="Face Powder">Face Powder</Option>
                    <Option value="Highlighter">Highlighter</Option>

                    <Option value="Concealer">Concealer</Option>
                    <Option value="Bronzer">Bronzer</Option>
                    <Option value="BB & CC Cream">BB & CC Cream</Option>
                    <Option value="Liquid Foundation">Liquid Foundation</Option>
                    <Option value="Blush">Blush</Option>
                    <Option value="Color Corrector">Color Corrector</Option>
                </Select >
            );
        }
        else if (this.state.category === "Lip Makeup") {
            select_subcategory.push(
                <Select
                    defaultValue="Lip Balm"
                    style={{ width: 160 }}
                    placeholder="Select a Lip Makeup!"
                    onChange={this.handleSubCategoryChange}
                    value={this.state.subcategory}>
                    <Option value="Lip Balm">Lip Balm</Option>
                    <Option value="Lip Plumper">Lip Plumper</Option>
                    <Option value="Lip Gloss">Lip Gloss</Option>
                    <Option value="Lipstick">Lip Lipstick</Option>
                    <Option value="Lip Liner">Lip Liner</Option>
                    <Option value="Lip Palettes">Lip Palettes</Option>
                </Select >
            );
        }
        else {
            select_subcategory.push(
                <Select
                    defaultValue="Eyebrow Makeup"
                    style={{ width: 160 }}
                    placeholder="Select a Eye Makeup!"
                    onChange={this.handleSubCategoryChange}
                    value={this.state.subcategory}>
                    <Option value="Eyebrow Makeup">Eyebrow</Option>
                    <Option value="Eye Liner">Eye Liner</Option>
                    <Option value="Eye Primer">Eye Primer</Option>
                    <Option value="Mascara">Mascara</Option>
                    <Option value="Eyeshadow Palette">Eyeshadow</Option>
                    <Option value="Eyeshadow">Eyeshadow</Option>
                    <Option value="Lash Serum">Lash Serum</Option>
                    <Option value="Brow Liner">Brow Liner</Option>
                    <Option value="Eyelash">Eyelash</Option>
                </Select >
            );
        }

        let return_result = [];
        if (this.state.loading === true) {

            if (this.state.product_id === null) {
                return_result.push(<div style={{"fontSize": "15px"}}>Please enter your search information
                    ... &nbsp;(*╹▽╹*)&nbsp;</div>);
            } else {
                return_result.push(<div style={{"fontSize": "15px"}}>Finding the similar products
                    ... &nbsp;(*╹▽╹*)&nbsp;</div>);
            }
        }
        else {
            // return_result.push(<Divider/>);
            if (this.state.product_id === null) {
                return_result.push(<div style={{"font-size": "15px"}}>
                    Here are the searching results of <b>{this.state.search_name}</b></div>);
            } else {
                return_result.push(<div style={{"fontSize": "15px"}}>Here are the similar products of <b>{this.state.product_name}</b></div>);
            }
            return_result.push(<div>&nbsp;&nbsp;</div>);
            return_result.push(<Radio.Group
                options={options}
                defaultValue="false"
                onChange=
                    {this.handleDisplayChange}
            />);
            return_result.push(<Divider/>);
            return_result.push(<div>&nbsp;&nbsp;</div>);
            if (this.state.is_neo === "false") {
                if (this.state.product_id === null) {
                    return_result.push(<TableList title={"Best Results for You ❤"} dataSource={this.state.response_data["Result"]}
                                                  handleHyperLinkClick = {this.handleHyperLinkClick}/>);
                } else {
                    return_result.push(<TableList title={"Best Results for You ❤"} dataSource={this.state.response_data["Top"]}
                                                  handleHyperLinkClick = {this.handleHyperLinkClick}/>);
                    return_result.push(<div>&nbsp;&nbsp;</div>);
                    return_result.push(<TableList title={"Worst Results for You 💔"} dataSource={this.state.response_data["Last"]}
                                                  handleHyperLinkClick = {this.handleHyperLinkClick}/>);
                }
            } else {
                return_result.push(<div style={{"fontSize": "15px"}}>TBD
                    ... &nbsp;(*╹▽╹*)&nbsp;</div>);
            }

        }

        return(
            <div id="page-wrapper">
                {/*<PageTitle title="Neo4J"/>*/}
                {/*<div className="row">*/}
                {/*    <Card title="Analysis the article and Visualize it" >*/}
                {/*        <div className="col-md-12">*/}
                {/*            <h5>Analysis the article and Visualize it</h5>*/}
                {/*            <div>Analysis the article and Visualize it.</div>*/}
                {/*        </div>*/}
                {/*    </Card>*/}

                {/*</div>*/}

                <div className="App-header">
                    {/*<img src={logo} className="App-logo" alt="logo"/>*/}
                    <h1>Search in MAKEUP PEDIA! </h1>

                </div>

                <div className="App-search">

                    <label htmlFor="category">
                        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Category &nbsp;&nbsp;
                        <Select
                            defaultValue="Face Makeup"
                            style={{ width: 160 }}
                            placeholder="Select a category"
                            onChange={this.handleCategoryChange}
                            value={this.state.category}>
                            <Option value="Face Makeup">Face Makeup 😊</Option>
                            <Option value="Lip Makeup">Lip Makeup 💄</Option>
                            <Option value="Eye Makeup">Eye Makeup 👁</Option>

                        </Select >
                    </label>

                    <label htmlFor="subcategory">
                        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Sub Category: &nbsp;&nbsp;
                        {select_subcategory}
                    </label>

                    <label htmlFor="search_name">
                        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Product Name: &nbsp;&nbsp;
                        <Input
                            id="search_name"
                            style={{ width: 500 }}
                            placeholder="Input the product name!"
                            onChange={this.handleSearchNameChange}
                            value={this.state.search_name}
                        />
                    </label>

                </div>

                <div className="App-header">

                    <Button onClick=
                                {this.handleGoBackClick}
                    >Go Back</Button>
                    &nbsp;&nbsp;&nbsp;&nbsp;
                    <Button type="primary" icon={<SearchOutlined />}
                            onClick= {this.handleSearchClick}
                    >Search</Button>
                    &nbsp;&nbsp;&nbsp;&nbsp;
                    <Button onClick=
                                {this.handleResetClick}
                    >Reset</Button>
                    &nbsp;&nbsp;&nbsp;&nbsp;
                    <Button onClick=
                                {this.handleAutoFillClick}
                    >Example</Button>

                </div>
                <div className="App-body">
                    <div style={{"fontSize": "13px"}}>{return_result}</div>
                </div>

            </div>




        );
    }
}

export default Search;
