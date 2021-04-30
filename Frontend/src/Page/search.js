import React from 'react';
import * as D3 from 'd3';
import {event as CurrentEvent} from 'd3';

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
                return_result.push(<div style={{"fontSize": "15px"}}>
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
                    let currentComponent = this;
                    return_result.push(<svg  style={{'width':1200,'height':'900'}}  id="disGraphSvg" ></svg>);

                    axios.post('http://localhost:8000/search_graph',{
                        id: currentComponent.state.response_data.ID
                    }, {
                        headers: {
                            "Access-Control-Allow-Origin" : "",
                            "Allow": "POST",
                            "Content-type": "Application/json"
                        }
                    }).then(function (response) {
                            let data = response.data;
                            let initScale = 1;
                            let relations_names = [
                                'BELONGS_TO', 'CONTAINS','HAS_CONCERNS','HAS_CONS',
                                'HAS_PROS', 'HAS_USER_TAG','IN_COLOR','IS_BEST_FOR',
                                'PRODUCED_BY','PURCHASE_FROM', 'SUBCLASS_OF'
                            ];
                            let relations_colors = [
                                '#636059','#636059','#636059','#636059',
                                '#636059','#636059','#636059','#636059',
                                '#636059','#636059','#636059'
                            ];
                            let names = [
                                'BestFor','Brand','Category','Colors',
                                'Concerns', 'Cons','Ingredient', 'Product',
                                'Pros', 'PurchaseLink', 'Subcategory', 'UserTags'
                            ];
                            let colors = [
                                '#B6E2D3', '#FAE8E0', '#B6E2D3', '#FBE5C8',
                                '#FADCD9', '#F79489', '#A31563', '#EF7C8E',
                                '#669DBA', '#B8D0DD', '#FCDCA9', '#B8D0DD',
                            ];

                            		        	    //全图缩放器
		        		var zoom = D3.zoom()
		        		.scaleExtent([0.25,2])
		        		.on("zoom",zoomFn);

		        		var svg = D3.select("#disGraphSvg");
		        		//var width = svg.attr("width");
		        		var width = 1200;
		        		var height = 1000;
		        		svg.call(zoom).on('dbclick.zoom',null);
		        		//缩放层
		        		var container = svg.append("g")
		        		.attr('transform','scale(' + initScale + ')')
		        		.attr('class','container');



		        		var relation = [];
		        		var labels = [];

		        		var nodes_data = data.nodes;
		        		var edges_data = data.links;
		        		console.log(nodes_data);
		        		console.log(edges_data);

		        		//关系去重
		        		for(var i=0; i<edges_data.length; i++){
		        			if(relation.indexOf(edges_data[i].relation) == -1){
		        				relation.push(edges_data[i].relation);
		        			}
		        		}
		        		//标签去重
		        		for(var i=0; i<nodes_data.length; i++){
		        			if(labels.indexOf(nodes_data[i].label) == -1){
		        				labels.push(nodes_data[i].label);
		        			}
		        		}

		        		edges_data.forEach(function(link){
		        			nodes_data.forEach(function(node){
		        				if(link.source == node.inst_cd){
		        					link.source = node;
		        				}
		        				if(link.target == node.inst_cd){
		        					link.target = node;
		        				}
		        			})
		        		});


		        		//创建力图的模拟器
		        		var forceSimulation = D3.forceSimulation()
		        		.force("link",D3.forceLink().distance(200).strength(1))
		        		.force("charge",D3.forceManyBody().strength(-200))
                        .force('collide', D3.forceCollide(5))
		        		.force("center",D3.forceCenter(width/2,height/2));

		        		//转换节点数据
		        		forceSimulation.nodes(nodes_data)
		        		.on("tick",ticked);
		        		//转换连线数据
		        		forceSimulation.force("link")
		        		.links(edges_data)
		        		.distance(200 + Math.round(Math.random() * 50));

		        		//画连线
		        		var links = container.append("g")
		        		.attr("class","links")
	                    .selectAll("line")
	                    .data(edges_data)
	                    .enter()
	                    .append("line")
	                    .attr("stroke",function(d,i) {
        					return relations_colors[relations_names.indexOf(d.relation)];
        				})
	                    .attr("x1",function(n){return n.source.x})
	                    .attr("y1",function(n){return n.source.y})
	                    .attr("x2",function(n){return n.target.x})
	                    .attr("y2",function(n){return n.target.y})
	                    .attr("marker-end","url(#marker)");

		        		//画连线的文本
		        		var links_text = container.append("g")
		        		.attr("class","destexts")
	                    .selectAll("text")
	                    .data(edges_data)
	                    .enter()
	                    .append("text")
	                    .attr("x",function(e){
	                        return (e.source.x+e.target.x)/2;
	                    })
	                    .attr("y",function(e){
	                        return (e.source.y+e.target.y)/2;
	                    })
	                    .attr("fontSize",7)
	                    .text(function(e){return e.relation});


		        		//定义箭头
		        		container.append("svg:defs")
		        		.data(edges_data)
	                    .append("svg:marker")
	                    .attr("id", "marker")
	                    .attr('viewBox', '0 -5 10 10') //坐标系的区域
	                    .attr("refX", 20) //箭头坐标
	                    .attr("refY",0)
	                    .attr('markerWidth', 15) //标识大小
	                    .attr('markerHeight', 15)
	                    .attr('orient','auto') //绘制方向，可设定为：auto（自动确认方向）和 角度值
	                    .append('svg:path')
	                    .attr('d', 'M0,-5L10,0L0,5')  //箭头的路径
	                    .attr("fill","grey");

		        		//画节点组
		        		var nodes_g = container.append("g")
		        		.attr("class","nodes")
		        		.selectAll("circle")
	                    .data(nodes_data)
	                    .enter()
	                    .append("circle")
	                    .attr("transform",function(d,i){
	                    	var cirX = d.x;
	                    	var cirY = d.y;
	                    	return "translate("+cirX + ","+cirY+")";
	                    })
	                    .attr("r",40)
	                    .attr("fill",function(d,i){
	                    	return colors[names.indexOf(d.label)];
	                    })
	                    .attr("name",function(d){
        					return d.name;
        				})
/*	                    .attr("fill",function(d) {
		        			return colors[names.indexOf(d.label)];*/
	                    .call(D3.drag()
	                        .on("start",started)
	                        .on("drag",dragged)
	                        .on("end",ended));
        				//画节点
        				/*nodes_g.append("circle").attr("r",15).attr("fill",function(d,i){
        					return colors[names.indexOf(d.label)];
        				}).attr("name",function(d){
        					return d.name;
        				});*/


        				//画节点本文
        				var nodes_text = container.append("g")
        				.attr("class","nodes")
        				.selectAll("text")
        				.data(nodes_data)
        				.enter()
	                    .append("text")
	                    .attr("x",function(e){
	                    	return e.x;
	                    })
	                    .attr("y",function(e){
		                    return e.y;
	                    })
	                    .attr("dx",-30)
	                    .attr("dy",5)
//	                    .attr("transform",function(d,i){
//	                    	var dx = d.x;
//	                    	var dy = d.y;
//	                    	return "translate("+ dx + ","+ dy +")";
//	                    })
        				.attr("font-size",13)
                        .style("central")
        				.attr('name',function(d){return d.name;}).text(function(e){return e.name});

		        		//该变量保证拖动鼠标时，不会影响图形变换，默认为false未选中鼠标
		        		var dragging = false;

		        		 function started(d){
		                     if(!D3.event.active){
		                         forceSimulation.alpha(0.8).restart(); //.alphaTarget(0.3).restart();
		                     }
		                     d.fx = d.x;
		                     d.fy = d.y;
		                     dragging = true;
		                 }
		                 function dragged(d){
		                     d.fx = D3.event.x;
		                     d.fy = D3.event.y;
		                 }
		                 function ended(d) {
		                     if(!D3.event.active){
		                         forceSimulation.alpha(0.8);//alphaTarget(0);
		                     }
		                     d.fx = null;
		                     d.fy = null;
		                     dragging = false;
		                 }

		                 function ticked(){
		                     links
		                         .attr("x1",function(n){return n.source.x})
		                         .attr("y1",function(n){return n.source.y})
		                         .attr("x2",function(n){return n.target.x})
		                         .attr("y2",function(n){return n.target.y})
		                     links_text
		                         .attr("x",function(e){
		                             return (e.source.x+e.target.x)/2;
		                         })
		                         .attr("y",function(e){
		                             return (e.source.y+e.target.y)/2;
		                         })
		                     nodes_g
		                     .attr("transform", function(d) {
			        				return "translate(" + d.x + "," + d.y + ")";
			        			});
		                     nodes_text
		                     .attr("x",function(e){return e.x})
		                     .attr("y",function(e){return e.y})
		                 }

		                 function zoomFn() {
		                	    const {
		                	        transform,
		                	        scale
		                	    } = D3.event;
		                	    container.attr('transform',  transform);
		                	}

                    })
                
                    $('#disGraphSvg').on('mouseenter', '.nodes circle', function(event) {
                        //通过变量dragging保证拖动鼠标时，其状态不受影响，从而改变图形
                        //鼠标没有拖动才能处理事件
                        if(!dragging) {
                            //获取被选中元素的名字
                            var name = $(this).attr("name");
                            //选择#svg1 .nodes中所有的circle，再增加个class
                            D3.select('#disGraphSvg .nodes').selectAll('circle').attr('class', function(d) {
                                //数据的id是否等于name,返回空
                                if(d.name==name) {
                                    return '';
                                } 
                                //当前节点返回空，否则其他节点循环判断是否被隐藏起来(CSS设置隐藏)
                                else {
                                    //links链接的起始节点进行判断,如果其id等于name则显示这类节点
                                    //注意: graph=data
                                    for (var i = 0; i < edges_data.length; i++) {
                                        //如果links的起点等于name，并且终点等于正在处理的则显示
                                        if (edges_data[i]['source'].name == name && edges_data[i]['target'].name == d.name) {
                                            return '';
                                        }
                                        if (edges_data[i]['target'].name == name && edges_data[i]['source'].name == d.name) {
                                            return '';
                                        }
                                    }
                                
                                    return "inactive"; //前面CSS定义 .nodes circle.inactive
                                }
                            });

                            //处理相邻的边line是否隐藏 注意 || 
                            D3.select("#disGraphSvg .links").selectAll('line').attr('class', function(d) {
                                if (d.source.name == name || d.target.name == name) {
                                    return '';
                                } else {
                                    return 'inactive';
                                }
                            });
                            
                            //隐藏箭头
                            D3.select("#disGraphSvg .links").selectAll('line').attr('marker-end', function(d) {
                                if (d.source.name == name || d.target.name == name) {
                                    return 'url(#marker)';
                                } else {
                                    return '';
                                }
                            });
                            
                            //处理相邻的文字是否隐藏 注意 || 
                            D3.select("#disGraphSvg").selectAll('.destexts text').attr('class', function(d) {
                                if (d.source.name == name || d.target.name == name) {
                                    return '';
                                } else {
                                    return 'inactive';
                                }
                            });
                            
                            //处理相邻的文字是否隐藏 注意 || 
                            D3.select("#disGraphSvg").selectAll('.nodes text').attr('class', function(d) {
                                if (d.name == name) {
                                    return '';
                                } else {
                                    for (var i = 0; i < edges_data.length; i++) {
                                        //如果links的起点等于name，并且终点等于正在处理的则显示
                                        if (edges_data[i]['source'].name == name && edges_data[i]['target'].name == d.name) {
                                            return '';
                                        }
                                        if (edges_data[i]['target'].name == name && edges_data[i]['source'].name == d.name) {
                                            return '';
                                        }
                                    }
                                
                                    return "inactive"; //前面CSS定义 .nodes circle.inactive
                                }
                            });
                        }
                       });

                    //鼠标移开还原原图，显示所有隐藏的点及边
                    $('#disGraphSvg').on('mouseleave', 'circle', function(event) {
                        //如果dragging为false才处理事件
                        if(!dragging) {
                            D3.select('#disGraphSvg').selectAll('.nodes circle').attr('class', '');
                            D3.select('#disGraphSvg').selectAll('.links line').attr('marker-end', 'url(#marker)');
                            D3.select('#disGraphSvg').selectAll('.links line').attr('class', '');
                            D3.select('#disGraphSvg').selectAll('.destexts text').attr('class','');
                            D3.select('#disGraphSvg').selectAll('.nodes text').attr('class','');
                        } 
                    });

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
