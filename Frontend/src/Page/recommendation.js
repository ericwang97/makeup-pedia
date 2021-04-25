import React from 'react';
import PageTitle from '../Component/page-title.js';
import './home.css'
import { Card } from "antd";
import 'antd/es/card/style/css'; // 加载 CSS

class Recommendation extends React.Component{


    render(){
        return(
            <div id="page-wrapper">
                <PageTitle title="Personalize your news!"/>
                <div className="row">
                    <Card title="Personalize your news and get the Recommendation!" >
                        <div className="col-md-12">
                            <h5>Personalize your news and get the Recommendation!</h5>
                            <div>Try to favorite something, and I will update the database and send more accurate news results for you.</div>
                        </div>
                    </Card>

                </div>
            </div>


        );
    }
}

export default Recommendation;
