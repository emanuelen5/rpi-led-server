import React, { Component } from "react";
import $ from 'jquery';

class App extends Component {
    constructor(props) {
        super(props);
        this.state = {
        };
        this.update = this.update.bind(this);
        this.update("/api/display", 200);
        this.update("/api/settings", 500);
    }

    update(endpoint, timeout_ms=500) {
        const setstate_cb = data => {
            this.setState(data);
        };
        const cb = () => {
            console.debug(`Running cb for ${endpoint}`);
            $.get(endpoint).then(setstate_cb);
            setTimeout(cb, timeout_ms);
        };
        cb();
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
