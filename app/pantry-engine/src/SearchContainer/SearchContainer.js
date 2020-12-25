import * as React from "react";
import RecipeCard from "../RecipeCard/RecipeCard";
import CardSlide from "../RecipeCardSlide/Slide"
import CardSlideItem from "../RecipeCardSlide/CardSlide";
import'./SearchContainer.css'
import CardIngredientList from "../RecipeCard/CardIngredientList/CardIngredientList";


class SearchContainer extends React.Component {
    constructor(props) {
        super(props);
    }

    renderSquare(result) {

        console.log(result.url)
        let items = [{
                cardName: result.title,
                available_ingredients: result.available_ingredients,
                unavailable_ingredients: result.unavailable_ingredients,
                showBodyImage: true,
                bodyImage: result.image_url,
                authorName: result.author_name,
                showRating: true,
                rating: result.rating
            },{
                cardName: 'Steps',
                showSteps: true,
                steps: result.steps
        }, {
            cardName: "Nutrition Information",
            showRating: true,
            rating: result.rating,
            showNutrition: true,
            nutrition_info: result.nutrition_info
            }
        ];
        return (

            <CardSlide url={result.url} items={items}/>
        )
    }

    render() {
        console.log(this.props.result)
        return (
                <div>
                  {this.props.result.map((result, index) => (
                      <div key={index}>
                          <div style={{
                              display: 'flex',
                              alignItems: 'center',
                              justifyContent: 'center',
                          }}>
                              {this.renderSquare(result)}
                          </div>
                      </div>
                  ))}
                </div>




        )
    }
}
//
// <RecipeCard recipe_title={result.title}
//             recipe_url={result.url}
//             recipe_img={result.image_url}
//             available_ingredients={result.available_ingredients}
//             unavailable_ingredients={result.unavailable_ingredients}/>

export default SearchContainer;