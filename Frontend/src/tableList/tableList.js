import {Button, Card, Rate, Table} from "antd";
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
                        return (<img src={link[0]} style={{ width: 180, height: 180 }}
                        />
                        )}
                },
                {
                    title: 'Product',
                    dataIndex: 'product_names',
                    id: 'name',
                    width: 250,
                    render: text => {
                        let url = "https://www.beautypedia.com/products/" + text.replaceAll(" ", "-");
                        return (<a href={url}
                        >{text}
                        </a>)
                    }
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
                    width: 100,
                    render: text => {
                        let url = "https://www.beautypedia.com/?s=" + text.replaceAll(" ", "-");
                        return (<a href={url}
                        >{text}
                        </a>)
                    }
                },
                {
                    title: 'Price 💲',
                    width: 80,
                    // dataIndex: 'price',
                    render: (text, record) => {
                        if (record.buy_url.length === 0) {
                            return (<span>{record.price}</span>)
                        } else {
                            return (<span>{record.price} <a href={record.buy_url}
                            > 🛒 </a> </span>)
                        }
                    }
                },
                {
                    title: 'MakeUp Alley Reviews 💬',
                    width: 250,
                    render: (text, record) => {
                        if (record.mua_url.length === 0) {
                            return (
                                <div>
                                    <Rate disabled allowHalf
                                        //autoFocus={true}
                                          defaultValue={record.mua_rating //.toFixed(1)
                                          }/>&nbsp;&nbsp;
                                    <span> {record.mua_review_cnt} 💬 </span>
                                </div>
                            )
                        } else {
                            return (
                                <div>
                                    <Rate disabled allowHalf
                                          defaultValue={record.mua_rating}/>&nbsp;&nbsp;
                                    <span> <a href={record.mua_url}>{record.mua_review_cnt} 💬</a></span>
                                </div>
                            )
                        }

                    }},
                    {
                        title: 'EWG Concerns 🧪',
                        width: 220,
                        render: (text, record) => {
                            if ('overall_concerns' in record) {
                                let Colors={'HIGH':'FireBrick','MODERATE':'SandyBrown','LOW_MODERATE':'Khaki','LOW':'MediumAquaMarine'};
                                return (
                                <div>
                                    <li>
                                        <span>Cancer: </span>
                                        <strong style={{color: Colors[record.overall_concerns.Cancer]}}>{record.overall_concerns.Cancer} </strong>
                                    </li>
                                    <li>
                                        <span>Toxicity: </span>
                                        <strong style={{color: Colors[record.overall_concerns['Developmental & reproductive toxicity']]}}>{record.overall_concerns['Developmental & reproductive toxicity']} </strong>
                                    </li>
                                    <li>
                                        <span>Allergies: </span>
                                        <strong style={{color: Colors[record.overall_concerns['Allergies & immunotoxicity']]}}>{record.overall_concerns['Allergies & immunotoxicity']}</strong>
                                    </li>
                                    </div>
                                )
                            } else {
                                return (
                                    <div>
                                        Not Available 😞
                                    </div>
                                )
                            }

                        }},
                {
                    title: 'Find Similar',
                    dataIndex: 'product_id',
                    render: (text, record) => {
                        return (<Button className="Button"
                                        onClick={this.props.handleHyperLinkClick.bind(this, text, record.product_names)}
                        >Find it!
                        </Button>)
                    }
                },
            ]

        }

    }

    drawQueryTable(){
        //let columnName = eval(this.props.columnName);
        return (<Card title={this.props.title}>
            <Table //className="ant-table"
                columns={this.state.response_data}
                   dataSource={this.props.dataSource}
                   bordered
                //defaultPageSize={1}
                   minRows={20}
                   size="small"
                   //pagination={{simple: true}}
                pagination={{ pageSize: 5 }}
                   scroll={{ y: 1000 }}
                   loading={this.props.loading}
            >
            </Table>

        </Card>)
    }

    drawSearchTable(){

        return (<Card title={this.props.title} style={{ width: 1350 }}>
            <Table className="ant-table"
                   columns={this.state.response_data}
                dataSource={this.props.dataSource}
                bordered
                //defaultPageSize={1}
                minRows={20}
                size="small"
                //pagination={{simple: true}}
                   pagination={{ pageSize: 5 }}
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
