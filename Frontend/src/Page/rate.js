import React from 'react';
import PageTitle from '../Component/page-title.js';
import './home.css'
import { Card, Input, Rate,Button } from "antd";
import 'antd/es/rate/style/css';
import axios from "axios";
import TableList from "../tableList/tableList"; // 加载 CSS
const { Search } = Input;


class myRate extends React.Component{

    constructor(props) {
        super(props);

        this.state = {
            loading:true,
            rate: "",
            comment: "",
            msg:"",
        };
        this.handleRateChange = this.handleRateChange.bind(this);
        this.handleCommentChange = this.handleCommentChange.bind(this);
        this.handleDataSending = this.handleDataSending.bind(this);

    }

    handleDataSending(){
        let currentComponent = this;

        //let url2 = "http://13.57.28.139:8000/rate?rate=" + currentComponent.state.rate +
        //    "&comment=" + currentComponent.state.comment;
        let url = "http://13.57.28.139:8000/rate";
        let rate = currentComponent.state.rate
        let comment = currentComponent.state.comment

        axios.post(url,{
            rate:rate,
            comment:comment
        })
            .then(function (response) {
                let msg = response.data.msg;
                let status = response.data.status;

                if (status === 0) {
                    currentComponent.setState({
                        loading: false, msg: msg
                    });

                } else {
                    alert(msg);
                }
            })
            .catch(function (error) {
                alert("error");
                console.log(error);

            });
    }

    handleRateChange(value) {
        this.setState({rate: value, loading: true});
    }
    handleCommentChange(event) {
        //console.log(value)
        this.setState({comment: event.target.value, loading: true});
    }

    render(){

        let returnResult = [];

        if (this.state.loading === false){
            returnResult.push(<div>&nbsp;&nbsp;</div>)
            returnResult.push(<div>{this.state.msg}</div>)
        }

        return(
            <div id="page-wrapper">
                <div className="row">
                    <div>&nbsp;&nbsp;</div>
                    <div>&nbsp;&nbsp;</div>
                    <Card title="Rate it and leave some advices (*╹▽╹*)" >
                        <div className="col-md-12">
                            <h5>I will be very appreciate if you could leave some comments here for me. I will improve myself for sure. Thank you!</h5>
                            <Rate allowHalf
                                  //autoFocus={true}
                                  defaultValue={0}
                                  onChange={value => this.handleRateChange(value)}/>
                            <div>&nbsp;&nbsp;</div>
                            <Input
                                placeholder="Input your comments here"
                                //enterButton="send"
                                //size="large"
                                style={{ width: 400 }}
                                onChange={this.handleCommentChange}
                                value={this.state.comment}/>
                            <div>&nbsp;&nbsp;</div>
                            <Button
                                type="primary"
                                onClick=
                                        {this.handleDataSending}
                            >Send</Button>



                        </div>
                    </Card>

                    <div style={{"fontSize": "13px"}}>{returnResult}</div>

                </div>
            </div>


        );
    }
}

export default myRate;
