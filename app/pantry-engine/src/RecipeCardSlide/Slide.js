import React from 'react';
import CardSlideItem from './CardSlide';
import './card-slide.scss';

class CardSlide extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            items: this.props.items,
            cardSelected: 1,
            slideAnimation: 'slide-left'
        }
        this.renderStateProps = this.renderStateProps.bind(this);
        this.updateRenderStateProps = this.updateRenderStateProps.bind(this);
        this.chooseCardSlideItem = this.chooseCardSlideItem.bind(this);
        this.nextItem = this.nextItem.bind(this);
        this.prevItem = this.prevItem.bind(this);
    }


    renderStateProps() {
        try {
            const state = Object.assign({}, this.state);
            for (let key in this.props) {
                if (state.hasOwnProperty(key)) {
                    state[key] = this.props[key];
                }
            }
            this.setState(state);
        }
        catch(error) {
            return;
        }
    }


    chooseCardSlideItem(slideItem) {
        try {
            this.setState({
                cardSelected: slideItem+1,
                slideAnimation: slideItem+1 < this.state.cardSelected ? 'slide-right' : 'slide-left'
            });
        }
        catch(error) {
            return;
        }
    }

    prevItem() {
        if (this.state.cardSelected === 1) return false;
        try {
            this.setState({
                cardSelected: this.state.cardSelected-1,
                slideAnimation: 'slide-right'
            });
        }
        catch(error) {
            return;
        }
    }


    nextItem() {
        if (this.state.cardSelected === this.state.items.length) return false;
        try {
            this.setState({
                cardSelected: this.state.cardSelected+1,
                slideAnimation: 'slide-left'
            });
        }
        catch(error) {
            return;
        }
    }

    updateRenderStateProps = (prevProps) => {
        try {
            if (prevProps !== this.props) {
                const state = Object.assign({}, this.state);
                for (let key in this.state) {
                    if (this.props.hasOwnProperty(key) && this.props[key] !== prevProps[key]) {
                        state[key] = this.props[key];
                    }
                }
                this.setState(state);
                // reset card slide item to the first card
                if (this.state.cardSelected === 2) {
                    this.chooseCardSlideItem(0)
                }
                if (this.state.cardSelected === 3) {
                    this.chooseCardSlideItem(0)
                }
            } else {
                return false;
            }
        }
        catch(error) {
            return false;
        }
    }

    componentDidUpdate(prevProps) {
        this.updateRenderStateProps(prevProps);
    }

    componentDidMount() {
        this.renderStateProps();
    }

    componentWillReceiveProps({items}) {
        this.setState({...this.state,items});
    }

    render() {
        try {
            const { items, cardSelected, slideAnimation } = this.state;
            return (<div className='card-slide'>
                <div className='card-slide-container'>
                    {items.map( (item, key) => {
                        if (key === (cardSelected-1)) {
                            item.isSelected = true;
                            item.slideAnimation = slideAnimation;
                        } else {
                            item.isSelected = false;
                        }
                        item.itemKey = key;
                        return <CardSlideItem url={this.props.url} key={key} {...item}/>
                    })}
                    {items.length > 1 && cardSelected > 1 && <a className='prev' onClick={this.prevItem}>❮</a>}
                    {items.length > cardSelected && <a className='next' onClick={this.nextItem}>❯</a>}
                </div>
                <div className='card-dot'>
                    {items.length > 1 && items.map((item, key) => {
                        return <span className={`dot ${cardSelected-1 === key && 'active'}`} key={key} onClick={() => this.chooseCardSlideItem(key)} />
                    })}

                </div>
            </div>);
        }
        catch(error) {
            return (
                <div>{error.message}</div>
            );
        }
    }
}

export default CardSlide;