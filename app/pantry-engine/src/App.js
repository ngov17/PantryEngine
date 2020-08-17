import React from 'react';
import './App.css';
import NavbarPantry from "./NavbarPantry/NavbarPantry";
import SearchPantry from "./SearchPantry/SearchPantry";
import Container from "react-bootstrap/cjs/Container";
import Logo from "./Logo/Logo";
import TestCardWrapper from "./TestCardWrapper/TestCardWrapper";
import Subtext from "./Subtext/Subtext";
import SearchContainer from "./SearchContainer/SearchContainer";

function App() {
  return (
    <div className="App">
          <NavbarPantry/>
          <div className={'logo-subtext-container'}>
              <Logo className='mb-4'/>
              <Subtext query={'A search engine for food.'}/>
          </div>
        <SearchContainer/>
    </div>
  );
}

export default App;
