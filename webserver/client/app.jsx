import React, { Component } from "react";
import $ from 'jquery';

class App extends Component {
    constructor(props) {
        super(props);
        this.state = {
        };
        this.update = this.update.bind(this);
        setTimeout(this.update, 500);
    }

    update() {
        $.get("/settings").then(data => {
            this.setState(data);
            setTimeout(this.update, 500);
        });
    }

	render() {
        let objs = [];
        Object.entries(this.state).forEach(([key, value]) => {
            objs.push(value);
        });
		return (
            <>
            REACT STUFF :D
            <ol> { objs.map((idx, i) => <li key={i}> {JSON.stringify(idx)} </li>) } </ol>
            </>
		);
	}
};

export default App;
