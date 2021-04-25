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
            category: null,
            subcategory: null,
            age: null,
            skin_type: null,
            skin_color: null,
            hair_style: null,
            hair_color: null,
            eye_color: null,
            top_k: null,

            loading: true,
            response_data: null

        };
        this.handleSearchClick = this.handleSearchClick.bind(this);
        this.handleResetClick = this.handleResetClick.bind(this);

        this.handleCategoryChange = this.handleCategoryChange.bind(this);
        this.handleSubCategoryChange = this.handleSubCategoryChange.bind(this);
        this.handleAgeChange = this.handleAgeChange.bind(this);
        this.handleSkinTypeChange = this.handleSkinTypeChange.bind(this);
        this.handleSkinColorChange = this.handleSkinColorChange.bind(this);
        this.handleHairStyleChange = this.handleHairStyleChange.bind(this);
        this.handleHairColorChange = this.handleHairColorChange.bind(this);
        this.handleEyeColorChange = this.handleEyeColorChange.bind(this);
        this.handleTopKChange = this.handleTopKChange.bind(this);
    }

    handleSearchClick() {
        let currentComponent = this;
        // let base_url = "http://13.57.28.139:8000/";
        let url = "http://localhost:8000/recommend";

        axios.post(url,{
            category: currentComponent.state.category,
            subcategory: currentComponent.state.subcategory,
            age: currentComponent.state.age,
            skin: currentComponent.state.skin_type,
            skin_color: currentComponent.state.skin_color,
            hair: currentComponent.state.hair_style,
            hair_color: currentComponent.state.hair_color,
            eye: currentComponent.state.eye_color,
            top_k: currentComponent.state.top_k
        })
            .then(function (response) {
                let status = response.data.status;
                if (status === 0) {
                    let response_data = response.data.response
                    currentComponent.setState({
                        loading: false, response_data: response_data
                    });

                } else {
                    alert(response.data.msg);
                }
            })
            .catch(function (error) {
                alert("error");
                console.log(error);

            });

    }

    handleResetClick() {
        this.setState({
            category: null,
            subcategory: null,
            age: null,
            skin_type: null,
            skin_color: null,
            hair_style: null,
            hair_color: null,
            eye_color: null,
            top_k: null,
            loading: true,
            response_data: null
        })
    }

    handleCategoryChange(value) {
        this.setState({category: value, loading: true, subcategory: null});
    }
    handleSubCategoryChange(value) {
        this.setState({subcategory: value, loading: true});
    }
    handleAgeChange(value) {
        this.setState({age: value, loading: true});
    }

    handleSkinTypeChange(value) {
        this.setState({skin_type: value, loading: true});
    }

    handleSkinColorChange(value) {
        this.setState({skin_color: value, loading: true});
    }

    handleHairStyleChange(value) {
        this.setState({hair_style: value, loading: true});
    }

    handleHairColorChange(value) {
        this.setState({hair_color: value, loading: true});
    }

    handleEyeColorChange(value) {
        this.setState({eye_color: value, loading: true});
    }

    handleTopKChange(event) {
        this.setState({top_k: event.target.value, loading: true});
    }

    render() {

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

            return_result.push(<div>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</div>)
            return_result.push(<div style={{"fontSize": "15px"}}>Please enter your information
                    ... &nbsp;(*╹▽╹*)&nbsp;</div>);
        }
        else {
            return_result.push(<div>&nbsp;&nbsp;</div>);

            return_result.push(<div style={{"font-size": "15px"}}>Searching results
                of: {this.state.subcategory} </div>);

            return_result.push(<div>&nbsp;&nbsp;</div>);
            // return_result.push(<TableList tableName={table}
            //                              columnName={columnName}
            //                              dataSource={this.state.response_data[table][PK]}
            //                              handleHyperLinkClick = {this.handleHyperLinkClick}/>);
        }

        return (

            <div id="page-wrapper">
                <div className="App-header">
                    {/*<img src={logo} className="App-logo" alt="logo"/>*/}
                    <h1>Guess What You Like! </h1>

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
                            <Option value="Face Makeup">Face Makeup</Option>
                            <Option value="Lip Makeup">Lip Makeup</Option>
                            <Option value="Eye Makeup">Eye Makeup</Option>

                        </Select >
                    </label>

                    <label htmlFor="subcategory">
                        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Sub Category: &nbsp;&nbsp;
                        {select_subcategory}
                    </label>

                </div>

                <div className="App-search">
                    <label htmlFor="age">
                        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Age &nbsp;&nbsp;
                        <Select
                            defaultValue="19-24"
                            style={{ width: 160 }}
                            placeholder="Select Your Age"
                            onChange={this.handleAgeChange}
                            value={this.state.age}>
                            <Option value="Under 18">Under 18</Option>
                            <Option value="19-24">19-24</Option>
                            <Option value="25-29">25-29</Option>
                            <Option value="30-35">30-35</Option>
                            <Option value="36-43">36-43</Option>
                            <Option value="44-55">44-55</Option>
                            <Option value="56 & Over">56 & Over</Option>


                        </Select >
                    </label>

                    <label htmlFor="skin_type">
                        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Skin Type &nbsp;&nbsp;
                        <Select
                            defaultValue="Combination"
                            style={{ width: 160 }}
                            placeholder="Select Skin Type"
                            onChange={this.handleSkinTypeChange}
                            value={this.state.skin_type}>
                            <Option value="Very Dry">Very Dry</Option>
                            <Option value="Dry">Dry</Option>
                            <Option value="Medium">Medium</Option>
                            <Option value="Fair-Medium">Fair Medium</Option>
                            <Option value="Fair">Fair</Option>
                            <Option value="Combination">Combination</Option>
                            <Option value="Oily">Oily</Option>
                            <Option value="Very Oily">Very Oily</Option>
                            <Option value="Sensitive">Sensitive</Option>
                            <Option value="Acne-prone">Acne Prone</Option>
                            <Option value="Normal">Normal</Option>
                            <Option value="Neutral">Neutral</Option>

                        </Select >
                    </label>

                    <label htmlFor="skin_color">
                        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Skin Color &nbsp;&nbsp;
                        <Select
                            defaultValue="Normal"
                            style={{ width: 160 }}
                            placeholder="Select Skin Color"
                            onChange={this.handleSkinColorChange}
                            value={this.state.skin_color}>
                            <Option value="Olive">Olive</Option>
                            <Option value="Normal">Normal</Option>
                            <Option value="Warm">Warm</Option>
                            <Option value="Medium Brown">Medium Brown</Option>
                            <Option value="Tan">Tan</Option>
                            <Option value="Dark">Dark</Option>
                            <Option value="Deep Dark">Deep Dark</Option>

                        </Select >
                    </label>

                    <label htmlFor="hair_style">
                        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Hair Style &nbsp;&nbsp;
                        <Select
                            defaultValue="Straight"
                            style={{ width: 160 }}
                            placeholder="Select Hair Style"
                            onChange={this.handleHairStyleChange}
                            value={this.state.hair_style}>
                            <Option value="Straight">Straight</Option>
                            <Option value="Fine">Fine</Option>
                            <Option value="Medium">Medium</Option>
                            <Option value="Curly">Curly</Option>
                            <Option value="Coarse">Coarse</Option>
                            <Option value="Relaxed">Relaxed</Option>

                        </Select >
                    </label>

                    <label htmlFor="hair_color">
                        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Hair Color &nbsp;&nbsp;
                        <Select
                            defaultValue="Black"
                            style={{ width: 160 }}
                            placeholder="Select Hair Color"
                            onChange={this.handleHairColorChange}
                            value={this.state.hair_color}>
                            <Option value="Black">Black</Option>
                            <Option value="Brown">Brown</Option>
                            <Option value="Grey">Grey</Option>
                            <Option value="Silver">Silver</Option>
                            <Option value="Red">Red</Option>
                            <Option value="Brunette">Brunette</Option>
                            <Option value="Blond">Blond</Option>

                        </Select >
                    </label>

                    <label htmlFor="eye_color">
                        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Eye Color &nbsp;&nbsp;
                        <Select
                            defaultValue="Black"
                            style={{ width: 160 }}
                            placeholder="Select Eye Color"
                            onChange={this.handleEyeColorChange}
                            value={this.state.eye_color}>
                            <Option value="Black">Black</Option>
                            <Option value="Brown">Brown</Option>
                            <Option value="Blue">Blue</Option>
                            <Option value="Violet">Violet</Option>
                            <Option value="Gray">Gray</Option>
                            <Option value="Green">Green</Option>
                            <Option value="Hazel">Hazel</Option>
                            <Option value="Other">Other</Option>

                        </Select >
                    </label>
                </div>
                <div className="App-search">
                    <label htmlFor="topK">
                        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Top K &nbsp;&nbsp;
                        <Input
                            id="topK"
                            style={{ width: 300 }}
                            placeholder="Return TopK Results, 1 ~ 10"
                            onChange={this.handleTopKChange}
                            value={this.state.top_k}
                        />
                    </label>

                </div>
                <div className="App-header">

                    <Button type="primary" icon={<SearchOutlined />}
                            onClick= {this.handleSearchClick}
                    >Search</Button>
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    <Button onClick=
                                {this.handleResetClick}
                    >Reset</Button>

                </div>
                <div className="App-body">
                    <div style={{"fontSize": "13px"}}>{return_result}</div>
                </div>
            </div>

        );
    }
}

export default App;
