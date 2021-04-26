import {Button, Card, Table} from "antd";
import React from "react";
import 'antd/es/table/style/css'; // 加载 CSS
import 'antd/es/card/style/css'; // 加载 CSS
import './tableList.css';
//import 'antd/es/table/style'; // 加载 style

class TableList extends React.Component {
    constructor(props) {
        super(props);

        this.state = {

            response_data : [
                {
                    title:'Image',
                    dataIndex: 'image_url',
                    render: link => {
                        return (<img src={link[0]} style={{ width: 180 }}
                        />
                        )}
                },
                {
                    title: 'Product',
                    dataIndex: 'product_names',
                    id: 'name',
                    render: text => {
                        let url = "https://www.beautypedia.com/products/" + text.replaceAll(" ", "-");
                        return (<a href={url}
                        >{text}
                        </a>)
                    }
                },
                {
                    title: 'Category',
                    dataIndex: 'category'
                },
                {
                    title: 'Subcategory',
                    dataIndex: 'sub_category',
                    render: text => {
                        return  (<span>{text[0]}</span>)
                    }
                },
                {
                    title: 'Brand',
                    dataIndex: 'brand',
                    render: text => {
                        let url = "https://www.beautypedia.com/?s=" + text.replaceAll(" ", "-");
                        return (<a href={url}
                        >{text}
                        </a>)
                    }
                },
                {
                    title: 'Price',
                    dataIndex: 'price'
                },
                {
                    title: 'Where to Purchase',
                    dataIndex: 'buy_url',
                    render: text => {
                        if (text.length === 0) {
                            return ({})
                        } else {
                            return (<a href={text}
                            >Buy here!
                            </a>)
                        }
                    }},
                {
                    title: 'Look for Reviews',
                    dataIndex: 'buy_url',
                    render: text => {
                        if (text.length === 0) {
                            return ({})
                        } else {
                            return (<a href={text}
                            >See Reviews!
                            </a>)
                        }

                    }},
                {
                    title: 'Find Similar',
                    dataIndex: 'product_id',
                    render: text => {
                        return (<Button className="Button"
                                        onClick={this.props.handleHyperLinkClick.bind(this, text)}
                        >Find it!
                        </Button>)
                    }
                },
            ]

        }

    }

    drawQueryTable(){
        //let columnName = eval(this.props.columnName);
        return (<Card title={this.props.tableName}>
            <Table //className="ant-table"
                    columns={this.state[this.props.columnName]}
                   dataSource={this.props.dataSource}
                   bordered
                //defaultPageSize={1}
                   minRows={20}
                   size="small"
                   //pagination={{simple: true}}
                pagination={{ pageSize: 50 }}
                   scroll={{ y: 1000 }}
                   loading={this.props.loading}
            >
            </Table>

        </Card>)
    }

    drawSearchTable(){

        return (<Card title={this.props.tableName} style={{ width: 1350 }}>
            <Table className="ant-table"
                columns={this.state.response_data}
                dataSource={this.props.dataSource}
                bordered
                //defaultPageSize={1}
                minRows={20}
                size="small"
                //pagination={{simple: true}}
                pagination={true}
                loading={this.props.loading}
            >
            </Table>

        </Card>)
    }
    render() {
        if (this.props.page === "query"){
            return this.drawQueryTable();
        }
        else{
            return this.drawSearchTable();
        }

    }

}

export default TableList;

{/*<TableList*/}
{/*    handleHyperLinkClick = {}*/}
{/*    tableName={"countrylanguage"}*/}
{/*    columnName={"world_countrylanguage"}*/}
{/*    dataSource={[{"CountryCode":1,"Language":2,"IsOfficial":3,"Percentage":4}]}*/}
{/*/>*/}
