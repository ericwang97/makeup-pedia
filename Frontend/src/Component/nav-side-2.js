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
                                <Menu.Item key="crawler">
                                    <PieChartOutlined />
                                    <Link to='/crawler'><b>Run Crawler (TBD)</b></Link>
                                </Menu.Item>
                                <Menu.Item key="recommendation">
                                    <PieChartOutlined />
                                    <Link to='/recommendation'><b>Personalize News (TBD)</b></Link>
                                </Menu.Item>
                                <Menu.Item key="word-cloud">
                                    <PieChartOutlined />
                                    <Link to='/word-cloud'><b>Word Cloud (TBD)</b></Link>
                                </Menu.Item>


                                <SubMenu
                                    key="news"
                                    title={<span>
                                                <ContainerOutlined />
                                                <b>News</b>
                                              </span>
                                    }>
                                    <Menu.Item key="28"><Link to='/news-tweet'>Tweet</Link ></Menu.Item>
                                </SubMenu>
                                <SubMenu
                                    key="world"
                                    title={<span>
                                                <UserOutlined />
                                                DB example: World
                                              </span>
                                    }>
                                    <Menu.Item key="1"><Link to='/world-city'>City</Link ></Menu.Item>
                                    <Menu.Item key="2"><Link to='/world-country'>Country</Link ></Menu.Item>
                                    <Menu.Item key="3"><Link to='/world-countrylanguage'>Country Language</Link ></Menu.Item>
                                </SubMenu>
                                <SubMenu
                                    key="sakila"
                                    title={
                                        <span>
                                            <LaptopOutlined />
                                            DB example: Film
                                          </span>
                                    }>
                                    <Menu.Item key="4"><Link to='/sakila-film'>Film</Link ></Menu.Item>
                                    <Menu.Item key="5"><Link to='/sakila-actor'>Actor</Link ></Menu.Item>
                                    <Menu.Item key="6"><Link to='/sakila-film_actor'>Film&Actor</Link ></Menu.Item>

                                    <Menu.Item key="7"><Link to='/sakila-category'>Category</Link ></Menu.Item>
                                    <Menu.Item key="8"><Link to='/sakila-film_category'>Film&Category</Link ></Menu.Item>
                                    <Menu.Item key="9"><Link to='/sakila-film_text'>Film Text</Link ></Menu.Item>
                                    <Menu.Item key="10"><Link to='/sakila-language'>Film Language</Link ></Menu.Item>

                                    <Menu.Item key="11"><Link to='/sakila-address'>Address</Link ></Menu.Item>
                                    <Menu.Item key="12"><Link to='/sakila-city'>City</Link ></Menu.Item>
                                    <Menu.Item key="13"><Link to='/sakila-country'>Country</Link ></Menu.Item>
                                    <Menu.Item key="14"><Link to='/sakila-customer'>Customer</Link ></Menu.Item>
                                    <Menu.Item key="15"><Link to='/sakila-inventory'>Inventory</Link ></Menu.Item>
                                    <Menu.Item key="16"><Link to='/sakila-payment'>Payment</Link ></Menu.Item>
                                    <Menu.Item key="17"><Link to='/sakila-rental'>Rental</Link ></Menu.Item>
                                    <Menu.Item key="18"><Link to='/sakila-staff'>Staff</Link ></Menu.Item>
                                    <Menu.Item key="19"><Link to='/sakila-store'>Store</Link ></Menu.Item>

                                </SubMenu>
                                <SubMenu
                                    key="customers_order"
                                    title={
                                        <span>
                                            <NotificationOutlined />
                                            DB example: Customers Order
                                          </span>
                                    }>
                                    <Menu.Item key="20"><Link to='/customers_order-products'>Products</Link ></Menu.Item>
                                    <Menu.Item key="21"><Link to='/customers_order-customers'>Customers</Link ></Menu.Item>
                                    <Menu.Item key="22"><Link to='/customers_order-orderdetails'>Order details</Link ></Menu.Item>
                                    <Menu.Item key="23"><Link to='/customers_order-orders'>Orders</Link ></Menu.Item>
                                    <Menu.Item key="24"><Link to='/customers_order-payments'>Payments</Link ></Menu.Item>
                                    <Menu.Item key="25"><Link to='/customers_order-productlines'>Product lines</Link ></Menu.Item>
                                    <Menu.Item key="26"><Link to='/customers_order-employees'>Employees</Link ></Menu.Item>
                                    <Menu.Item key="27"><Link to='/customers_order-offices'>Offices</Link ></Menu.Item>
                                </SubMenu>
                            </Menu>
                        </Sider>
                    </Layout>

             </div>
        );
    }
}


export default NavSide;
