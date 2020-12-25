import * as React from "react";
import InputGroup from "react-bootstrap/InputGroup";
import FormControl from "react-bootstrap/FormControl";
import Form from "react-bootstrap/Form"
import 'bootstrap/dist/css/bootstrap.min.css';
import Button from "react-bootstrap/Button";
import './SearchPantry.css';
import SearchContainer from "../SearchContainer/SearchContainer";
import {trackPromise, usePromiseTracker} from "react-promise-tracker";
import Loader from 'react-loader-spinner';


// This is the loading indicator that is displayed while the asynchronous fetch is executed
const LoadingIndicator = (props) => {
    const { promiseInProgress } = usePromiseTracker();

    return (
        <div>
            {promiseInProgress === true &&
            <div style={{ width: "100%", height: "100", display: "flex", justifyContent: "center", alignItems: "center"
                 }}>

            <Loader type="ThreeDots" color="#363636" height="100" width="100" />
            </div>}
        </div>
    );
}

class SearchPantry extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            value: "",
            placeholder_default:  "Enter your ingredients!",
            result: [],
            queried: false
        }
    }

    callAPI(qry) {
        let url = "http://localhost:3001?q=" + qry
        trackPromise(fetch(url)
            .then(res => res.json())
            .then(res => this.setState({result: res, queried: true
            })));
    }

    handleSubmit = (e) => {
        this.setState({queried: true})
        const query = this.props.query || this.state.value ;
        //const values = query.split(" ");
        //alert('Query: ' + query)
        this.callAPI(query);
    }

    onTextChanged = (e) => {
        const text = e.target.value;
        if (text.length > 0) {
            this.setState(() => ({
                value: text
            }))
        }
    }

    handleKeyDown = (e) => {
        if (e.keyCode === 13) {
            this.handleSubmit(e)
        }
    }

    getContainerContents() {
        const indicator = <LoadingIndicator/>
        return (
            <div>
                {this.indicator}
                <SearchContainer queried={this.state.queried} result={this.state.result}/>
            </div>
        );
        // else {
        //     return (
        //         <>
        //             <SearchTemplate disabled={true} buttonClick={this.handleSubmit} value={'tomatoes, garlic, chicken, olives'}/>
        //         //             <SearchTemplate disabled={true} buttonClick={this.handleSubmit} value={'broccoli, asparagus, beef, chicken, a potato, toast'}/>
        //                    <SearchTemplate disabled={true} buttonClick={this.handleSubmit} value={'flour, leftover rice, carrots'}/>
        //         </>)
        // }


    }

    render() {
        return (
            <div>
                <div className={'searchbar'}>
                    <input type={'text'}
                           className={'search_input'}
                           onChange={this.onTextChanged}
                           onKeyDown={this.handleKeyDown}
                           placeholder={this.getPlaceholder()}/>
                    <button type={'submit'}
                            className={'search_button'}
                            onClick={this.handleSubmit}>Search</button>
                </div>
                {this.getContainerContents()}
            </div>


        )
    }

    getPlaceholder = () => {
        return this.props.query || this.state.placeholder_default;
    }
}

export default SearchPantry;