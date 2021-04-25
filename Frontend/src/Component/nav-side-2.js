import React from 'react';
import ReactDOM from 'react-dom';
import {Link, NavLink} from 'react-router-dom';
import 'antd/dist/antd.css';
import { Layout, Menu, Breadcrumb } from 'antd';
import { UserOutlined, LaptopOutlined, NotificationOutlined,ContainerOutlined, PieChartOutlined } from '@ant-design/icons';
import './nav-side-2.css';
const { SubMenu } = Menu;
const { Header, Content, Sider } = Layout;

class NavSide extends React.Component{
    constructor(props){
        super(props);
    }

    render(){
        return(
            <div className="navbar-default navbar-side">

                    <Layout style={{ minHeight: '100vh' }}>
                        <Sider width={300} className="site-layout-background" >
                            <Menu
                                mode="inline"
                                className="site-layout-background"
                                defaultSelectedKeys={['search']}
                                defaultOpenKeys={['news']}
                                theme="dark"
                                style={{ height: '133%', borderRight: 0 }}
                            >
                                <Menu.Item key="search">
                                    <PieChartOutlined />
                                    <Link to='/search'><b>Search</b></Link>
                                </Menu.Item>

                                <Menu.Item key="recommend">
                                    <ContainerOutlined />
                                    <Link to='/recommend'><b>Recommend</b></Link>
                                </Menu.Item>


                            </Menu>
                        </Sider>
                    </Layout>

             </div>
        );
    }
}


export default NavSide;
