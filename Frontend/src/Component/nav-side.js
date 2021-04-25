import React from 'react';
import {Link, NavLink} from 'react-router-dom';
import './theme.css';

class NavSide extends React.Component{
    constructor(props){
        super(props);
    }

    render(){
        return(
            <div className="navbar-default navbar-side">
                <div className="sidebar-collapse">
                    <ul className="nav">
                        <li>
                            <NavLink exact activeClassName = "active-menu" to = "/search">
                                <i className="fa fa-bar-chart-o"/>
                                <span>Search</span>
                            </NavLink>
                        </li>
                        <li className="active">
                            <Link to="/news-tweet">
                                <i className="fa fa-sitemap" data-toggle="collapse"/>
                                <span>News</span>
                                <span className="fa arrow"/>
                            </Link>

                            <ul className="nav nav-second-level collapse in">
                                <li>
                                    <NavLink to="/news-tweet" activeClassName="active-menu" >tweet</NavLink>
                                </li>
                            </ul>
                        </li>
                        <li className="active">
                            <Link to="/world-city">
                                <i className="fa fa-sitemap" data-toggle="collapse"/>
                                <span>world</span>
                                <span className="fa arrow"/>
                            </Link>

                            <ul className="nav nav-second-level collapse in">
                                <li>
                                    <NavLink to="/world-city" activeClassName="active-menu" >city</NavLink>
                                </li>
                                <li>
                                    <NavLink to="/world-country" activeClassName="active-menu">country</NavLink>
                                </li>
                                <li>
                                    <NavLink to="/world-countrylanguage" activeClassName="active-menu">countrylanguage</NavLink>
                                </li>
                            </ul>
                        </li>
                        <li className="active">
                            <Link to="/sakila-film">
                                <i className="fa fa-sitemap"/>
                                <span>sakila</span>
                                <span className="fa arrow"/>
                            </Link>
                            <ul className="nav nav-second-level collapse in">
                                <li>
                                    <NavLink to="/sakila-film" activeClassName="active-menu">film</NavLink>
                                </li>
                                <li>
                                    <NavLink to="/sakila-actor" activeClassName="active-menu">actor</NavLink>
                                </li>
                                <li>
                                    <NavLink to="/sakila-film_actor" activeClassName="active-menu">film_actor</NavLink>
                                </li>
                            </ul>
                        </li>
                        <li className="active">
                            <Link to="/customers_order-orders">
                                <i className="fa fa-sitemap"/>
                                <span>customers_order</span>
                                <span className="fa arrow"/>
                            </Link>
                            <ul className="nav nav-second-level collapse in">
                                <li>
                                    <NavLink to="/customers_order-orders" activeClassName="active-menu">orders</NavLink>
                                </li>
                                <li>
                                    <NavLink to="/customers_order-orderdetails" activeClassName="active-menu">orderdetails</NavLink>
                                </li>
                                <li>
                                    <NavLink to="/customers_order-products" activeClassName="active-menu">products</NavLink>
                                </li>
                            </ul>
                        </li>
                    </ul>

                </div>

            </div>
        );
    }
}


export default NavSide;
