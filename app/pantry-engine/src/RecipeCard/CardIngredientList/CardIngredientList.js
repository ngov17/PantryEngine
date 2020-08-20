import React from "react";
import './CardIngredientList.css';

class CardIngredientList extends React.Component {

    getListOfIngredients = () => {
        return (
            <div>
            {
                this.props.ingredients.map((item, index) => (
                    <IngredientItem available={this.props.available} name={item}/>
                ))
            }
                {console.log(this.props.ingredients)}
            </div>

        )
    }

    render() {
        return (
            <div className={'ingredient-list'}>
                {this.getListOfIngredients()}
            </div>
        )
    }
}

class IngredientItem extends React.Component {
    getAvailable = () => {
        if (this.props.available) {
            return 'ingredient-available';
        }   else {
            return 'ingredient-unavailable';
        }
    }


    render() {
        return(
            <div className={'ingredient-item ' + this.getAvailable()}>
                {this.props.name}
            </div>
        )
    }
}

export default CardIngredientList;
