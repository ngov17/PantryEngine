import React from "react";
import './CardIngredientList.css';

class CardIngredientList extends React.Component {

    getListOfIngredients = () => {
        return (
            <div>
            {
                this.props.ingredients.map((item, index) => (
                    <IngredientItem name={item}/>
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
    render() {
        return(
            <div className={'ingredient-item'}>
                <p>{this.props.name}</p>
            </div>
        )
    }
}

export default CardIngredientList;
