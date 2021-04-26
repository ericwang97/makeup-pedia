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
                    title: 'product_names',
                    dataIndex: 'product_names'
                },
                {
                    title: 'category',
                    dataIndex: 'category'
                },
                {
                    title: 'sub_category',
                    dataIndex: 'sub_category'
                },
                {
                    title: 'brand',
                    dataIndex: 'brand'
                },
                {
                    title: 'product_links',
                    dataIndex: 'product_links',
                    render: text => {
                        return (<a href={text}
                        >product_link
                        </a>)
                }},
                {
                    title: 'price',
                    dataIndex: 'price'
                },
                {
                    title: 'buy_url',
                    dataIndex: 'buy_url',
                    render: text => {
                        return (<a href={text}
                        >buy this!
                        </a>)
                }},
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

        return (<Card title={this.props.subcategory} style={{ width: 1050 }}>
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
