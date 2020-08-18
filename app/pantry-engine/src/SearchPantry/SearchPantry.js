import * as React from "react";
import InputGroup from "react-bootstrap/InputGroup";
import FormControl from "react-bootstrap/FormControl";
import Form from "react-bootstrap/Form"
import 'bootstrap/dist/css/bootstrap.min.css';
import Button from "react-bootstrap/Button";
import './SearchPantry.css';
import SearchContainer from "../SearchContainer/SearchContainer";

class SearchPantry extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            value: "",
            placeholder_default:  "Enter your ingredients!",
            disabled: false,
            result: []
        }
    }


    callAPI(qry) {
        let url = "http://localhost:3001?q=" + qry
        fetch(url)
            .then(res => res.json())
            .then(res => this.setState({result: res
                }))
    }

    handleSubmit = (e) => {
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
            alert('enter clicked');
            this.handleSubmit(e)
        }
    }

    render() {
        return(
            //TODO: Turn to non-bootstrap.
            this.newSearch()
        )
    }

    getPlaceholder = () => {
        return this.props.query || this.state.placeholder_default;
    }





    newSearch() {
        return (
            <div>
                <div className={'searchbar'}>
                    <input type={'text'}
                           className={'search_input'}
                           onChange={this.onTextChanged}
                           onKeyDown={this.handleKeyDown}
                           disabled={this.props.disabled}
                           placeholder={this.getPlaceholder()}/>
                    <button type={'submit'}
                            className={'search_button'}
                            onClick={this.handleSubmit}>Search</button>
                </div>
                <SearchContainer result={this.state.result}/>

            </div>
        )
    }

    bootstrapSearch() {
        return (
            <div className={'searchbar'}>
                <InputGroup className={'mb-2'} onChange={this.onTextChanged} onKeyDown={this.handleKeyDown}>
                    <FormControl
                        placeholder={this.getPlaceholder}
                        aria-label="Ingredient list"
                        disabled={this.props.disabled}
                    />
                    <InputGroup.Append>
                        <Button type={'submit'} value={'Search!'} onClick={this.handleSubmit} >Search!</Button>
                    </InputGroup.Append>
                </InputGroup>
            </div>
        )
    }
}

export default SearchPantry;