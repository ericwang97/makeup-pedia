import React from "react";

import TableList from '../tableList/tableList.js';
import {Button} from "antd";
import axios from "axios";


class QueryTable extends React.Component{
    constructor(props) {
        super(props);
        this.state = {
            loading:true,
            database:"",
            table:"",
            searchwords:"",
            queryData: [],

            rating_rating : [
                {
                    title: 'Rating',
                    dataIndex: 'Rating'
                },
                {
                    title: 'Comment',
                    dataIndex: 'Comment'
                },
                {
                    title: 'Created Time',
                    dataIndex: 'Created_time'
                }
            ],

            news_tweet : [
                {
                    title: 'Topic',
                    dataIndex: 'topic'
                },
                {
                    title: 'UserName',
                    dataIndex: 'user_name'
                },
                {
                    title: 'Time',
                    dataIndex: 'created_time'
                },
                {
                    title: 'Favorite',
                    dataIndex: 'favorite_count',

                },
                {
                    title: 'Keywords',
                    dataIndex: 'keywords'
                },
                {
                    title: 'URL',
                    dataIndex: 'url'
                },
                {
                    title: 'Tweet',
                    dataIndex: 'text'
                }
            ],

            world_city : [
                {
                    title: 'ID',
                    dataIndex: 'ID'
                },
                {
                    title: 'Name',
                    dataIndex: 'Name'
                },
                {
                    title: 'CountryCode',
                    dataIndex: 'CountryCode',
                    //render: text => <a>{text}</a>,
                    render: text => {
                        return (<Button className="Button"
                                        onClick={this.props.handleHyperLinkClick.bind(this, "country", text)}
                        >{text}
                        </Button>)
                    }

                },
                {
                    title: 'District',
                    dataIndex: 'District'
                },
                {
                    title: 'Population',
                    dataIndex: 'Population'
                }
            ],
            world_country : [
                {
                    title: 'Code',
                    dataIndex: 'Code'
                },
                {
                    title: 'Name',
                    dataIndex: 'Name'
                },
                {
                    title: 'Continent',
                    dataIndex: 'Continent'
                },
                {
                    title: 'GovernmentForm',
                    dataIndex: 'GovernmentForm'
                },
                {
                    title: 'HeadOfState',
                    dataIndex: 'HeadOfState'
                },
                {
                    title: 'Region',
                    dataIndex: 'Region'
                },
                {
                    title: 'Capital',
                    dataIndex: 'Capital'
                },
                {
                    title: 'Population',
                    dataIndex: 'Population'
                },
                {
                    title: 'GNP',
                    dataIndex: 'GNP'
                },
                {
                    title: 'SurfaceArea',
                    dataIndex: 'SurfaceArea'
                }
            ],
            world_countrylanguage : [
                {
                    title: 'CountryCode',
                    dataIndex: 'CountryCode',
                    render: text => {
                        return (<Button className="Button"
                                        onClick={this.props.handleHyperLinkClick.bind(this, "country", text)}
                        >{text}
                        </Button>)
                    }
                },
                {
                    title: 'Language',
                    dataIndex: 'Language'
                },
                {
                    title: 'IsOfficial',
                    dataIndex: 'IsOfficial'
                },
                {
                    title: 'Percentage',
                    dataIndex: 'Percentage'
                }
            ],

            sakila_actor : [
                {
                    title: 'actor_id',
                    dataIndex: 'actor_id'
                },
                {
                    title: 'first_name',
                    dataIndex: 'first_name'
                },
                {
                    title: 'last_name',
                    dataIndex: 'last_name',

                }
            ],
            sakila_address : [
                {
                    title: 'address_id',
                    dataIndex: 'address_id'
                },
                {
                    title: 'address',
                    dataIndex: 'address'
                },
                {
                    title: 'district',
                    dataIndex: 'district',
                },
                {
                    title: 'city_id',
                    dataIndex: 'city_id',
                    //render: text => <a>{text}</a>,
                    render: text => {
                        return (<Button className="Button"
                                        onClick={this.props.handleHyperLinkClick.bind(this, "city", text)}
                        >{text}
                        </Button>)
                    }

                },
                {
                    title: 'postal_code',
                    dataIndex: 'postal_code'
                },
                {
                    title: 'phone',
                    dataIndex: 'phone'
                }
            ],
            sakila_category : [
                {
                    title: 'category_id',
                    dataIndex: 'category_id'
                },
                {
                    title: 'name',
                    dataIndex: 'name'
                }
            ],
            sakila_city : [
                {
                    title: 'city_id',
                    dataIndex: 'city_id'
                },
                {
                    title: 'city',
                    dataIndex: 'city'
                },
                {
                    title: 'country_id',
                    dataIndex: 'country_id',
                    //render: text => <a>{text}</a>,
                    render: text => {
                        return (<Button className="Button"
                                        onClick={this.props.handleHyperLinkClick.bind(this, "country", text)}
                        >{text}
                        </Button>)
                    }
                }
            ],
            sakila_country : [
                {
                    title: 'country_id',
                    dataIndex: 'country_id'
                },
                {
                    title: 'country',
                    dataIndex: 'country'
                }
            ],
            sakila_customer : [
                {
                    title: 'customer_id',
                    dataIndex: 'customer_id'
                },
                {
                    title: 'store_id',
                    dataIndex: 'store_id',
                    //render: text => <a>{text}</a>,
                    render: text => {
                        return (<Button className="Button"
                                        onClick={this.props.handleHyperLinkClick.bind(this, "store", text)}
                        >{text}
                        </Button>)
                    }
                },
                {
                    title: 'first_name',
                    dataIndex: 'first_name'
                },
                {
                    title: 'last_name',
                    dataIndex: 'last_name'
                },
                {
                    title: 'email',
                    dataIndex: 'email'
                },
                {
                    title: 'address_id',
                    dataIndex: 'address_id',
                    //render: text => <a>{text}</a>,
                    render: text => {
                        return (<Button className="Button"
                                        onClick={this.props.handleHyperLinkClick.bind(this, "address", text)}
                        >{text}
                        </Button>)
                    }
                }
            ],
            sakila_film : [
                {
                    title: 'film_id',
                    dataIndex: 'film_id'
                },
                {
                    title: 'title',
                    dataIndex: 'title'
                },
                {
                    title: 'description',
                    dataIndex: 'description'
                },
                {
                    title: 'release_year',
                    dataIndex: 'release_year'
                },
                {
                    title: 'language_id',
                    dataIndex: 'language_id',
                    //render: text => <a>{text}</a>,
                    render: text => {
                        return (<Button className="Button"
                                        onClick={this.props.handleHyperLinkClick.bind(this, "language", text)}
                        >{text}
                        </Button>)
                    }
                },
                {
                    title: 'rental_duration',
                    dataIndex: 'rental_duration'
                },
                {
                    title: 'rental_rate',
                    dataIndex: 'rental_rate'
                },
                {
                    title: 'length',
                    dataIndex: 'length'
                },
                {
                    title: 'replacement_cost',
                    dataIndex: 'rental_rate'
                },
                {
                    title: 'rating',
                    dataIndex: 'rating'
                },
                {
                    title: 'special_feature',
                    dataIndex: 'special_feature'
                }
            ],
            sakila_film_actor : [
                {
                    title: 'actor_id',
                    dataIndex: 'actor_id',
                    //render: text => <a>{text}</a>,
                    render: text => {
                        return (<Button className="Button"
                                        onClick={this.props.handleHyperLinkClick.bind(this, "actor", text)}
                        >{text}
                        </Button>)
                    }
                },
                {
                    title: 'film_id',
                    dataIndex: 'film_id',
                    //render: text => <a>{text}</a>,
                    render: text => {
                        return (<Button className="Button"
                                        onClick={this.props.handleHyperLinkClick.bind(this, "film", text)}
                        >{text}
                        </Button>)
                    }
                }
            ],
            sakila_film_category : [
                {
                    title: 'film_id',
                    dataIndex: 'film_id',
                    //render: text => <a>{text}</a>,
                    render: text => {
                        return (<Button className="Button"
                                        onClick={this.props.handleHyperLinkClick.bind(this, "film", text)}
                        >{text}
                        </Button>)
                    }
                },
                {
                    title: 'category_id',
                    dataIndex: 'category_id',
                    //render: text => <a>{text}</a>,
                    render: text => {
                        return (<Button className="Button"
                                        onClick={this.props.handleHyperLinkClick.bind(this, "category", text)}
                        >{text}
                        </Button>)
                    }
                }
            ],
            sakila_film_text : [
                {
                    title: 'film_id',
                    dataIndex: 'film_id',
                    //render: text => <a>{text}</a>,
                    render: text => {
                        return (<Button className="Button"
                                        onClick={this.props.handleHyperLinkClick.bind(this, "film", text)}
                        >{text}
                        </Button>)
                    }
                },
                {
                    title: 'title',
                    dataIndex: 'title'
                },
                {
                    title: 'description',
                    dataIndex: 'description',
                }

            ],
            sakila_inventory : [
                {
                    title: 'inventory_id',
                    dataIndex: 'inventory_id',
                },
                {
                    title: 'film_id',
                    dataIndex: 'film_id',
                    //render: text => <a>{text}</a>,
                    render: text => {
                        return (<Button className="Button"
                                        onClick={this.props.handleHyperLinkClick.bind(this, "film", text)}
                        >{text}
                        </Button>)
                    }
                },
                {
                    title: 'store_id',
                    dataIndex: 'store_id',
                    //render: text => <a>{text}</a>,
                    render: text => {
                        return (<Button className="Button"
                                        onClick={this.props.handleHyperLinkClick.bind(this, "store", text)}
                        >{text}
                        </Button>)
                    }
                }

            ],
            sakila_language : [
                {
                    title: 'language_id',
                    dataIndex: 'language_id'
                },
                {
                    title: 'name',
                    dataIndex: 'name'
                }
            ],
            sakila_payment : [
                {
                    title: 'payment_id',
                    dataIndex: 'payment_id'
                },
                {
                    title: 'customer_id',
                    dataIndex: 'customer_id',
                    //render: text => <a>{text}</a>,
                    render: text => {
                        return (<Button className="Button"
                                        onClick={this.props.handleHyperLinkClick.bind(this, "customer", text)}
                        >{text}
                        </Button>)
                    }
                },
                {
                    title: 'staff_id',
                    dataIndex: 'staff_id',
                    //render: text => <a>{text}</a>,
                    render: text => {
                        return (<Button className="Button"
                                        onClick={this.props.handleHyperLinkClick.bind(this, "staff", text)}
                        >{text}
                        </Button>)
                    }

                    //onChange={this.handleClickPKChange}
                },
                {
                    title: 'rental_id',
                    dataIndex: 'rental_id',
                    //render: text => <a>{text}</a>,
                    render: text => {
                        return (<Button className="Button"
                                        onClick={this.props.handleHyperLinkClick.bind(this, "rental", text)}
                        >{text}
                        </Button>)
                    }

                },
                {
                    title: 'amount',
                    dataIndex: 'amount'
                },
                {
                    title: 'payment_date',
                    dataIndex: 'payment_date'
                }
            ],
            sakila_rental : [
                {
                    title: 'rental_id',
                    dataIndex: 'rental_id'
                },
                {
                    title: 'rental_date',
                    dataIndex: 'rental_date'
                },
                {
                    title: 'inventory_id',
                    dataIndex: 'inventory_id',
                    //render: text => <a>{text}</a>,
                    render: text => {
                        return (<Button className="Button"
                                        onClick={this.props.handleHyperLinkClick.bind(this, "inventory", text)}
                        >{text}
                        </Button>)
                    }

                    //onChange={this.handleClickPKChange}
                },
                {
                    title: 'customer_id',
                    dataIndex: 'customer_id',
                    //render: text => <a>{text}</a>,
                    render: text => {
                        return (<Button className="Button"
                                        onClick={this.props.handleHyperLinkClick.bind(this, "customer", text)}
                        >{text}
                        </Button>)
                    }
                },
                {
                    title: 'return_date',
                    dataIndex: 'return_date'
                },
                {
                    title: 'staff_id',
                    dataIndex: 'staff_id',
                    //render: text => <a>{text}</a>,
                    render: text => {
                        return (<Button className="Button"
                                        onClick={this.props.handleHyperLinkClick.bind(this, "staff", text)}
                        >{text}
                        </Button>)
                    }
                }
            ],
            sakila_staff : [
                {
                    title: 'staff_id',
                    dataIndex: 'staff_id'
                },
                {
                    title: 'first_name',
                    dataIndex: 'first_name'
                },
                {
                    title: 'last_name',
                    dataIndex: 'last_name'
                },
                {
                    title: 'address_id',
                    dataIndex: 'address_id',
                    //render: text => <a>{text}</a>,
                    render: text => {
                        return (<Button className="Button"
                                        onClick={this.props.handleHyperLinkClick.bind(this, "address", text)}
                        >{text}
                        </Button>)
                    }

                    //onChange={this.handleClickPKChange}
                },
                {
                    title: 'email',
                    dataIndex: 'email'
                },
                {
                    title: 'store_id',
                    dataIndex: 'store_id',
                    //render: text => <a>{text}</a>,
                    render: text => {
                        return (<Button className="Button"
                                        onClick={this.props.handleHyperLinkClick.bind(this, "store", text)}
                        >{text}
                        </Button>)
                    }
                },
                {
                    title: 'username',
                    dataIndex: 'username'
                },
                {
                    title: 'password',
                    dataIndex: 'password'
                },
            ],
            sakila_store : [
                {
                    title: 'store_id',
                    dataIndex: 'store_id'
                },
                {
                    title: 'manager_staff_id',
                    dataIndex: 'manager_staff_id',
                    //render: text => <a>{text}</a>,
                    render: text => {
                        return (<Button className="Button"
                                        onClick={this.props.handleHyperLinkClick.bind(this, "staff", text)}
                        >{text}
                        </Button>)
                    }
                },
                {
                    title: 'address_id',
                    dataIndex: 'address_id',
                    //render: text => <a>{text}</a>,
                    render: text => {
                        return (<Button className="Button"
                                        onClick={this.props.handleHyperLinkClick.bind(this, "address", text)}
                        >{text}
                        </Button>)
                    }

                    //onChange={this.handleClickPKChange}
                }
            ],

            customers_order_customers : [
                {
                    title: 'customerNumber',
                    dataIndex: 'customerNumber'
                },
                {
                    title: 'customerName',
                    dataIndex: 'customerName'
                },
                {
                    title: 'contactFirstName',
                    dataIndex: 'contactFirstName'
                },
                {
                    title: 'contactLastName',
                    dataIndex: 'contactLastName'
                },
                {
                    title: 'phone',
                    dataIndex: 'phone'
                },
                {
                    title: 'addressLine1',
                    dataIndex: 'addressLine1'
                },
                {
                    title: 'addressLine2',
                    dataIndex: 'addressLine2'
                },
                {
                    title: 'city',
                    dataIndex: 'city'
                },
                {
                    title: 'state',
                    dataIndex: 'state',
                },
                {
                    title: 'postalCode',
                    dataIndex: 'postalCode'
                },
                {
                    title: 'country',
                    dataIndex: 'country'
                },
                {
                    title: 'salesRepEmployeeNumber',
                    dataIndex: 'salesRepEmployeeNumber'
                },
                {
                    title: 'creditLimit',
                    dataIndex: 'creditLimit'
                }
            ],
            customers_order_employees : [
                {
                    title: 'employeeNumber',
                    dataIndex: 'employeeNumber'
                },
                {
                    title: 'firstName',
                    dataIndex: 'firstName'
                },
                {
                    title: 'lastName',
                    dataIndex: 'lastName'
                },
                {
                    title: 'extension',
                    dataIndex: 'extension'
                },
                {
                    title: 'email',
                    dataIndex: 'email'
                },
                {
                    title: 'officeCode',
                    dataIndex: 'officeCode',
                    render: text => {
                        return (<Button className="Button"
                                        onClick={this.props.handleHyperLinkClick.bind(this, "offices", text)}
                        >{text}
                        </Button>)
                    }

                },
                {
                    title: 'reportsTo',
                    dataIndex: 'reportsTo'
                },
                {
                    title: 'jobTitle',
                    dataIndex: 'jobTitle'
                }
            ],
            customers_order_offices : [
                {
                    title: 'officeCode',
                    dataIndex: 'officeCode'
                },
                {
                    title: 'city',
                    dataIndex: 'city'
                },
                {
                    title: 'phone',
                    dataIndex: 'phone'
                },
                {
                    title: 'addressLine1',
                    dataIndex: 'addressLine1'
                },
                {
                    title: 'addressLine2',
                    dataIndex: 'addressLine2'
                },
                {
                    title: 'state',
                    dataIndex: 'state'
                },
                {
                    title: 'country',
                    dataIndex: 'country'
                },
                {
                    title: 'postalCode',
                    dataIndex: 'postalCode'
                },
                {
                    title: 'territory',
                    dataIndex: 'territory'
                }
            ],
            customers_order_orderdetails : [
                {
                    title: 'orderNumber',
                    dataIndex: 'orderNumber',
                    render: text => {
                        return (<Button className="Button"
                                        onClick={this.props.handleHyperLinkClick.bind(this, "orders", text)}
                        >{text}
                        </Button>)
                    }
                },
                {
                    title: 'orderLineNumber',
                    dataIndex: 'orderLineNumber'
                },
                {
                    title: 'productCode',
                    dataIndex: 'productCode',
                    render: text => {
                        return (<Button className="Button"
                                        onClick={this.props.handleHyperLinkClick.bind(this, "products", text)}
                        >{text}
                        </Button>)
                    }
                },
                {
                    title: 'quantityOrdered',
                    dataIndex: 'quantityOrdered',

                },
                {
                    title: 'priceEach',
                    dataIndex: 'priceEach'
                }
            ],
            customers_order_orders : [
                {
                    title: 'orderNumber',
                    dataIndex: 'orderNumber'
                },
                {
                    title: 'orderDate',
                    dataIndex: 'orderDate'
                },
                {
                    title: 'requiredDate',
                    dataIndex: 'requiredDate'
                },
                {
                    title: 'shippedDate',
                    dataIndex: 'shippedDate'
                },
                {
                    title: 'status',
                    dataIndex: 'status'
                },
                {
                    title: 'comments',
                    dataIndex: 'comments'
                },
                {
                    title: 'customerNumber',
                    dataIndex: 'customerNumber',
                    //render: text => <a>{text}</a>,
                    render: text => {
                        return (<Button className="Button"
                                        onClick={this.props.handleHyperLinkClick.bind(this, "customers", text)}
                        >{text}
                        </Button>)
                    }

                    //onChange={this.handleClickPKChange}
                }
            ],
            customers_order_payments : [
                {
                    title: 'customerNumber',
                    dataIndex: 'customerNumber',
                    //render: text => <a>{text}</a>,
                    render: text => {
                        return (<Button className="Button"
                                        onClick={this.props.handleHyperLinkClick.bind(this, "customers", text)}
                        >{text}
                        </Button>)
                    }
                },
                {
                    title: 'checkNumber',
                    dataIndex: 'checkNumber'
                },
                {
                    title: 'paymentDate',
                    dataIndex: 'paymentDate'
                },
                {
                    title: 'amount',
                    dataIndex: 'amount'
                }
            ],
            customers_order_productlines : [
                {
                    title: 'productLine',
                    dataIndex: 'productLine'
                },
                {
                    title: 'textDescription',
                    dataIndex: 'textDescription'
                }
            ],
            customers_order_products : [
                {
                    title: 'productCode',
                    dataIndex: 'productCode'
                },
                {
                    title: 'productName',
                    dataIndex: 'productName'
                },
                {
                    title: 'productLine',
                    dataIndex: 'productLine',
                    //render: text => <a>{text}</a>,
                    render: text => {
                        return (<Button className="Button"
                                        onClick={this.props.handleHyperLinkClick.bind(this, "productlines", text)}
                        >{text}
                        </Button>)
                    }

                    //onChange={this.handleClickPKChange}
                },
                {
                    title: 'productScale',
                    dataIndex: 'productScale'
                },
                {
                    title: 'productVendor',
                    dataIndex: 'productVendor'
                },
                {
                    title: 'productDescription',
                    dataIndex: 'productDescription'
                },
                {
                    title: 'quantityInStock',
                    dataIndex: 'quantityInStock'
                },
                {
                    title: 'buyPrice',
                    dataIndex: 'buyPrice'
                },
                {
                    title: 'MSRP',
                    dataIndex: 'MSRP'
                }
            ]
        }
        this.handleSearchHyperLinkClick = this.handleSearchHyperLinkClick.bind(this);
        this.handleHyperLinkClick = this.handleHyperLinkClick.bind(this);
        this.getTableData = this.getTableData.bind(this);
    }

    handleSearchHyperLinkClick() {
        let currentComponent = this;

        let url = "http://13.57.28.139:8000/query?databasename=" +
            currentComponent.state.database +
            "&tablelist=" + currentComponent.state.table +
            "&value=" + currentComponent.state.searchwords;

        axios.get(url)
            .then(function (response) {
                let status = response.data.status;

                if (status === 0) {
                    let data = response.data.data;
                    currentComponent.setState({loading: false, queryData: data});

                } else {
                    alert(response.data.msg);
                }
            })
            .catch(function (error) {
                alert("error");
                console.log(error);

            });

    }

    handleHyperLinkClick(table,searchwords) {
        let currentComponent = this;
        currentComponent.setState({
                table: table,
                loading: true,
                searchwords: searchwords},
            this.handleSearchHyperLinkClick);
        //currentComponent.setState(this.handleSearchHyperLinkClick);
    }

    componentWillReceiveProps(){
        let title = window.location.href.substring(window.location.origin.length + 1)

        let database = title.split("-")[0]
        let table = title.split("-")[1]

        this.getTableData(database,table);
    }

    componentDidMount(){

        let title = window.location.href.substring(window.location.origin.length + 1)

        let database = title.split("-")[0]
        let table = title.split("-")[1]

        this.getTableData(database,table);

    }
    // shouldComponentUpdate(nextProps, nextState, nextContext) {
    //     return true;
    // }


    getTableData(database,table){

        let currentComponent = this;
        let url = "http://13.57.28.139:8000/query?databasename=" + database +
            "&tablelist=" + table;
        currentComponent.setState({database:database,table:table,loading:true})
        axios.get(url)
            .then(function (response) {
                let status = response.data.status;
                console.log(response.data)
                if (status === 0) {
                    let data = response.data.data;
                    currentComponent.setState({queryData:data,loading:false})

                } else {
                    alert(response.data.msg);

                }
            }
            ).catch(function (error) {
            alert("error");
            console.log(error);

        });

    }

    render(){

        let columnName = this.state.database + "_" + this.state.table;

        return (
            <div id="page-wrapper">
                <TableList
                    handleHyperLinkClick = {this.handleHyperLinkClick}
                    tableName={this.state.table}
                    columnName={columnName}
                    page={"query"}
                    loading={this.state.loading}
                    dataSource={this.state.queryData}
                />
            </div>
        );
    }

}

export default QueryTable;
