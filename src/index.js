import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter as Router, Switch, Redirect, Route, Link} from 'react-router-dom';

import './index.css';
import Layout from './Component/layout.js';
import Home from './Page/home.js';
import App from './Page/App.js';
import QueryTable from './Page/queryTable.js';

import Recommendation from './Page/recommendation.js';
import Crawler from './Page/crawler.js';
import WordCloud from './Page/wordCloud.js';

import myRate from './Page/rate.js';
import Feature from './Page/feature.js';
import ErrorPage from './Page/error.js';
import * as serviceWorker from './serviceWorker';



class INF551DatabaseSearchEngine extends React.Component{
    render(){
        let LayoutRouter = (
            <Layout>
                <Switch>
                    <Route exact path="/" component = {Home}/>
                    <Route path="/search" component = {App}/>
                    <Route path="/recommendation" component = {Recommendation}/>
                    <Route path="/crawler" component = {Crawler}/>
                    <Route path="/word-cloud" component = {WordCloud}/>

                    <Route path="/rate" component = {myRate}/>
                    <Route path="/rating-rating" component = {QueryTable}/>
                    <Route path="/features" component = {Feature}/>

                    <Route path="/news-tweet" component = {QueryTable}/>

                    <Route path="/world-city" component = {QueryTable}/>
                    <Route path="/world-country" component = {QueryTable}/>
                    <Route path="/world-countrylanguage" component = {QueryTable}/>

                    <Route path="/sakila-film" component = {QueryTable}/>
                    <Route path="/sakila-actor" component = {QueryTable}/>
                    <Route path="/sakila-film_actor" component = {QueryTable}/>
                    <Route path="/sakila-category" component = {QueryTable}/>
                    <Route path="/sakila-film_category" component = {QueryTable}/>
                    <Route path="/sakila-film_text" component = {QueryTable}/>
                    <Route path="/sakila-language" component = {QueryTable}/>
                    <Route path="/sakila-address" component = {QueryTable}/>
                    <Route path="/sakila-city" component = {QueryTable}/>
                    <Route path="/sakila-country" component = {QueryTable}/>
                    <Route path="/sakila-customer" component = {QueryTable}/>
                    <Route path="/sakila-inventory" component = {QueryTable}/>
                    <Route path="/sakila-payment" component = {QueryTable}/>
                    <Route path="/sakila-rental" component = {QueryTable}/>
                    <Route path="/sakila-staff" component = {QueryTable}/>
                    <Route path="/sakila-store" component = {QueryTable}/>

                    <Route path="/customers_order-orders" component = {QueryTable}/>
                    <Route path="/customers_order-orderdetails" component = {QueryTable}/>
                    <Route path="/customers_order-products" component = {QueryTable}/>
                    <Route path="/customers_order-customers" component = {QueryTable}/>
                    <Route path="/customers_order-payments" component = {QueryTable}/>
                    <Route path="/customers_order-productlines" component = {QueryTable}/>
                    <Route path="/customers_order-employees" component = {QueryTable}/>
                    <Route path="/customers_order-offices" component = {QueryTable}/>

                    <Route component = {ErrorPage}/>
                </Switch>
            </Layout>
        )

        return(
            <Router>
                <Route path = "/"
                       render={ props => LayoutRouter }/>
            </Router>
        )
    }
}


ReactDOM.render(
  //<React.StrictMode>
    <INF551DatabaseSearchEngine />,
  //</React.StrictMode>,
  document.getElementById('app')
);

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
