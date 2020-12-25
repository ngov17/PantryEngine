import React from 'react';
import './card-slide-item.scss';
import CardIngredientList from "../RecipeCard/CardIngredientList/CardIngredientList";
import '../RecipeCard/CardIngredientList/CardIngredientList.css'
import Ratings from 'react-ratings-declarative';
import ScrollView, {ScrollElement} from "../RecipeCard/CardIngredientList/ScrollView";
import DataTable, { createTheme } from 'react-data-table-component';
import { BrowserRouter as Router, Switch, Route, Link } from 'react-router-dom';

class CardSlideItem extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            cardHeaderIcon: require('./images/Screen Shot 2020-08-09 at 4.12.02 PM.png'),
            cardName: 'Name of card: Title, Steps, etc',
            available_ingredients: [],
            unavailable_ingredients: [],
            cardData: [],
            cardGraphLineColor: '#30B1FF',
            cardGraphBgColor: '#D6EFFF',
            rendered: false,
            isSelected: true,
            slideAnimation: '',
            showBodyImage: false,
            showBodyText: true,
            authorName: 'author name',
            bodyImage: null,
            rating: null,
            showRating: false,
            steps: [],
            showSteps: false,
            nutrition_info:  null,
            showNutrition: false
        }

        this.renderStateProps = this.renderStateProps.bind(this);
        this.updateRenderStateProps = this.updateRenderStateProps.bind(this);
    }

    initalizeNutrition() {
        // initalize nutrition info if null
        if (this.isValidField(this.state.nutrition_info) === false) {
            return {
                calories: 'No Info',
                carbohydrates: 'No Info',
                fat: 'No Info',
                protein: 'No Info',
                sugar: 'No Info',
                fiber: 'No Info'
            }
        } else {
            return this.state.nutrition_info
        }
    }

    async renderStateProps() {
        try {
            const state = Object.assign({}, this.state);
            for (let key in this.props) {
                if (state.hasOwnProperty(key)) {
                    state[key] = this.props[key];
                }
            }
            state.rendered = true;
            this.setState(state);
        }
        catch(error) {
            return;
        }
    }


    updateRenderStateProps = (prevProps) => {
        if (this.state.rendered === false) return false;
        try {
            if (prevProps !== this.props) {
                const state = Object.assign({}, this.state);
                for (let key in this.state) {
                    if (this.props.hasOwnProperty(key) && this.props[key] !== prevProps[key]) {
                        state[key] = this.props[key];
                    }
                }
                this.setState(state);
            } else {
                return false;
            }
        }
        catch(error) {
            return false;
        }
    }

    componentDidMount() {
        this.renderStateProps();
    }

    componentDidUpdate(prevProps) {
        this.updateRenderStateProps(prevProps);
    }

    /**
     * function checks if input field is valid or not (null or undefined)
     */
    isValidField(field) {
        if(typeof field === 'undefined') {
            return false;
        } else if(field === null){
            return false;
        } else  {
            return true
        }
    }

    /**
     * function checks if input field is valid or not (null or undefined) and returns field
     * if it is
     */

    returnValidField(field) {
        if (this.isValidField(field)){
            return field
        } else {
            return 'No info'
        }
    }

    /**
     * function that renders each card's first page (with ingredients and picture)
     */
    renderIndexBody() {

        return (
            <div>
                <div className='leftbox'>
                    <div style={{
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                    }}>
                        <CardIngredientList available={true} ingredients={this.state.available_ingredients}/>
                    </div>
                </div>
                <div className='rightbox'>
                    <div style={{
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                    }}>
                        <CardIngredientList available={false} ingredients={this.state.unavailable_ingredients}/>
                    </div>
                </div>
            </div>

        );
    }

    /**
     * function that renders the second page of the card with steps
     */
    renderStepsBody() {
        return (

            <div className='steps'>
                <ScrollView ref={scroller2 => this._scroller = scroller2}>
                    <div className={'scroller2'}>
                        {
                            this.state.steps.map((step, index) => (
                                <ScrollElement>
                                    <div className='step'>
                                        <p>{step}</p>
                                    </div>
                                </ScrollElement>

                            ))
                        }
                    </div>
                </ScrollView>
            </div>

        );


    }

    /**
     * function that renders the third page of the card with steps
     */
    renderNutritionBody() {

        // initialize nutrition info
        const nutrition_info = this.initalizeNutrition()
        // theme for our table
        const theme = createTheme('theme', {
            text: {
                primary: 'deepyellow',
                secondary: '#2aa198'
            },
            background: {
                default: 'white'
            },
            context: {
                background: '#cb4b16',
                text: '#FFFFFF'
            },
            divider: {
                default: '#073642'
            }
        });
        // style
        const cellStyle = {
            cells: {
                style: {
                    fontSize: 'medium'
                }
            },
            headCells: {
                style: {
                    fontSize: 'large'
                }
            },
            table: {
                style: {

                }
            }
        }
        // define columns:
        const columns = [
            {
                name: 'Calories',
                selector: 'Calories'
            },
            {
                name: 'Carbohydrates',
                selector: 'Carbohydrates',
                right: true
            },
            {
                name: 'Fat',
                selector: 'Fat',
                right: true
            },
            {
                name: 'Protein',
                selector: 'Protein',
                right: true
            },
            {
                name: 'Sugar',
                selector: 'Sugar',
                right: true
            },
            {
                name: 'Fiber',
                selector: 'Fiber',
                right: true
            }
        ]
    // define the table
        let table = [{
            id: 1,
            Calories:this.returnValidField(nutrition_info.calories),
            Carbohydrates:this.returnValidField(nutrition_info.carbohydrates),
            Fat:this.returnValidField(nutrition_info.fat),
            Protein:this.returnValidField(nutrition_info.protein),
            Sugar:this.returnValidField(nutrition_info.sugar),
            Fiber:this.returnValidField(nutrition_info.fiber)

        }]

        return (

                <DataTable
                    title=''
                    columns={columns}
                    data={table}
                    theme='theme'
                    customStyles={cellStyle}
                />

        )
    }

    render() {
        try {
            const { cardHeaderIcon, cardName, available_ingredients, unavailable_ingredients,
                isSelected, slideAnimation, showBodyImage, bodyImage } = this.state;
            return (
                <div className={`card-slide-item ${isSelected === true ? ('enabled ' + slideAnimation) : 'disabled'}`}>
                    <div className='card'>
                        <div className='card-header'>
                                <div className='card-header-title' onClick={this.handleURLRedirect}>
                                    <a className={'url-text'}><Link to={'/'} style={{color:'#ffffff', fontSize:'medium'}}>
                                        {cardName}</Link></a>
                                </div>
                            {showBodyImage === true && <p className='author'>{('by ' + this.state.authorName)}</p>}
                            {this.state.showRating === true && this.isValidField(this.state.rating) === true &&
                            <div className='rating'>
                                <Ratings
                                    rating={this.state.rating}
                                    widgetDimensions="35px"
                                    widgetSpacings="8px"
                                >
                                    <Ratings.Widget widgetRatedColor="white" />
                                    <Ratings.Widget widgetRatedColor="white"  />
                                    <Ratings.Widget widgetRatedColor="white"  />
                                    <Ratings.Widget widgetRatedColor="white"  />
                                    <Ratings.Widget widgetRatedColor="white"  />
                                </Ratings>
                            </div>}
                        </div>
                        <div className='card-body'>
                            {(showBodyImage === true) && this.renderIndexBody()}
                            {this.state.showSteps === true && this.renderStepsBody()}
                            {this.state.showNutrition === true
                            && this.renderNutritionBody()}
                            {showBodyImage === true && <img className='middlebox' src={bodyImage} alt={''}/>}
                            <div className='card-body-graph'></div>
                        </div>
                        <div className='card-footer'></div>
                    </div>
                </div>
            );
        }
        catch(error) {
            return(
                <div className='card-slide'>
                    <div className='card'>
                        <div className='card-header'>
                            <div className='card-header-title'>Error</div>
                        </div>
                        <div className='card-body'>
                            <div className='card-body-description'>{error.message}</div>
                        </div>
                    </div>
                </div>
            );
        }
    }

    handleURLRedirect = () => {
        window.open(this.props.url) //to open new page;
    }
}

export default CardSlideItem;