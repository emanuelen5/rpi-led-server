import React, { Component } from "react";
import $ from 'jquery';

class App extends Component {
    constructor(props) {
        super(props);
        this.state = {
            "led_mode": "COLOR", 
            "led_settings": {
              "brightness": 1.0, 
              "color_index": 0, 
              "cycle_index": 0, 
              "speed": 0.01, 
              "strength": 1.0
            }, 
            "main_mode": "DEMO", 
            "select_mode": "MAIN_WINDOW"
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
