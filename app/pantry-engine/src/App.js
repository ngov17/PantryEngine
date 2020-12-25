import React from 'react';
import './App.css';
import NavbarPantry from "./NavbarPantry/NavbarPantry";
import SearchPantry from "./SearchPantry/SearchPantry";
import Logo from "./Logo/Logo";
import Subtext from "./Subtext/Subtext";
import AboutPage from "./About/About";
import { BrowserRouter as Router, Switch, Route, Link } from 'react-router-dom';

function App() {
  return (
    <div className="App">
        {/*<RecipeCard recipe_title={"Lorem Ipsum with a bunch of other stuff"}*/}
        {/*            recipe_url={'https://github.com/'}*/}
        {/*            recipe_img={'https://i2.wp.com/www.downshiftology.com/wp-content/uploads/2018/12/Shakshuka-19.jpg'}*/}
        {/*            available_ingredients={['Eggs', 'Tomatoes', 'Peppers', 'Onions']}*/}
        {/*            unavailable_ingredients={['Paprika', 'Sour cream', 'Pita bread']}/>*/}
        {/*<RecipeCard recipe_title={"Lorem Ipsum with a bunch of other stuff"}*/}
        {/*            recipe_url={'https://github.com/'}*/}
        {/*            recipe_img={'https://i2.wp.com/www.downshiftology.com/wp-content/uploads/2018/12/Shakshuka-19.jpg'}*/}
        {/*            available_ingredients={['Eggs', 'Tomatoes', 'Peppers', 'Onions']}*/}
        {/*            unavailable_ingredients={['Paprika', 'Sour cream', 'Pita bread']}/>*/}
        {/*<RecipeCard recipe_title={"Lorem Ipsum with a bunch of other stuff"}*/}
        {/*            recipe_url={'https://github.com/'}*/}
        {/*            recipe_img={'https://i2.wp.com/www.downshiftology.com/wp-content/uploads/2018/12/Shakshuka-19.jpg'}*/}
        {/*            available_ingredients={['Eggs', 'Tomatoes', 'Peppers', 'Onions']}*/}
        {/*            unavailable_ingredients={['Paprika', 'Sour cream', 'Pita bread']}/>*/}
        <Router>
            <div className="App">
                <NavbarPantry/>
                <div className={'logo-subtext-container'}>
                    <Logo className='mb-4'/>
                    <Subtext query={'A search engine for food.'}/>
                </div>

                <Switch>
                    <Route exact path={'/'} component={SearchPantry}/>
                    <Route exact path={'/about'} component={AboutPage}/>
                </Switch>
            </div>

        </Router>

    </div>
  );
}

export default App;
