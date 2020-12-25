import React from "react";
import './CardIngredientList.css';
import ScrollView, { ScrollElement } from "./ScrollView";

class CardIngredientList extends React.Component {

    getListOfIngredients = () => {
        return (
        <ScrollView ref={scroller => this._scroller = scroller}>
            <div className={'scroller'}>
            {
                this.props.ingredients.map((item, index) => (
                    <ScrollElement>
                        <IngredientItem available={this.props.available} name={item}/>
                    </ScrollElement>

                ))
            }
            </div>
        </ScrollView>

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
