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
import Search from './Page/search.js';
import Feature from './Page/feature.js';
import ErrorPage from './Page/error.js';
import * as serviceWorker from './serviceWorker';



class INF551DatabaseSearchEngine extends React.Component{
    render(){
        let LayoutRouter = (
            <Layout>
                <Switch>
                    <Route exact path="/" component = {Home}/>
                    <Route path="/recommend" component = {App}/>
                    <Route path="/search" component = {Search}/>
                    <Route path="/rate" component = {myRate}/>
                    <Route path="/features" component = {Feature}/>

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
