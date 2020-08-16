import * as React from "react";
import InputGroup from "react-bootstrap/InputGroup";
import FormControl from "react-bootstrap/FormControl";
import Form from "react-bootstrap/Form"
import 'bootstrap/dist/css/bootstrap.min.css';
import Button from "react-bootstrap/Button";
import './SearchPantry.css';
class SearchPantry extends React.Component {

    state = {
        value: "",
        placeholder_default:  "Enter your ingredients!",
        disabled: false
    }

    handleSubmit = (e) => {
        const query = this.props.query || this.state.value ;
        const values = query.split(" ");
        console.log(values);
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