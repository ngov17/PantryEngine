import * as React from "react";
import './RecipeCard.css';
import CardIngredientList from "./CardIngredientList/CardIngredientList";

class RecipeCard extends React.Component {

    handleClickCard = () => {
        window.location.href = this.props.recipe_url
    }

    render() {
        return(
            <div className={'item-padder'}>
                <div className={'recipe-card'} onClick={this.handleClickCard}>
                    <div className={'recipe-card-img'}>
                        <img className={'recipe-img'} src={this.props.recipe_img}/>
                    </div>
                    <div className={'recipe-card-ingredients'}>
                        <CardIngredientList ingredients={this.props.ingredients}/>
                    </div>
                    <div className={'recipe-card-footbar'}>
                        <a className={'recipe-card-title recipe-card-link'} href={this.props.recipe_url}>
                            {this.props.recipe_title}
                        </a>
                    </div>
                </div>
            </div>

        )
    }
}

export default RecipeCard;