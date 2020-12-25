import * as React from "react";
import './RecipeCard.css';
import CardIngredientList from "./CardIngredientList/CardIngredientList";


class RecipeCard extends React.Component {

    handleClickCard = () => {
        window.location.href = this.props.recipe_url
    }

    render() {
        let article = [{title: this.props.result.title, description: this.props.result.ingredients},
            {title: "STEPS", description: this.props.result.steps}];
        console.log(this.props.recipe_title)
        return(
            <div className={'recipe-item'}>
                <div className={'recipe-card'} onClick={this.handleClickCard}>
                    <div className={'recipe-card-img'}>
                        <img className={'recipe-img'} src={this.props.recipe_img}/>
                    </div>
                    <div className={'recipe-card-footbar'}>
                        <a className={'recipe-card-title recipe-card-link'} href={this.props.recipe_url}>
                            {this.props.recipe_title}
                        </a>
                    </div>
                </div>
                <div className={'ingredients'}>
                    <div className={'card-available-ingredients'}>
                        <CardIngredientList available={true} ingredients={this.props.available_ingredients}/>
                    </div>
                    <div className={'card-unavailable-ingredients'}>
                        <CardIngredientList available={false} ingredients={this.props.unavailable_ingredients}/>
                    </div>
                </div>
            </div>

        )
    }
}



export default RecipeCard;