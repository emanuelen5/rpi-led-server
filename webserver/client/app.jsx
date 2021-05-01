import React, { Component } from "react";
import $ from 'jquery';
import { io } from "socket.io/client-dist/socket.io";

class App extends Component {
    constructor(props) {
        super(props);
        this.state = {
        };
        this.update = this.update.bind(this);
        this.update("/api/display", 200);
        this.update("/api/settings", 500);

        const socket = io.connect('http://localhost:5000/socket');
        socket.on('after connect', function(msg) {
            console.log('After connect', msg);
        });
    }

    update(endpoint, timeout_ms=500) {
        const setstate_cb = data => {
            this.setState(data);
        };
        const cb = () => {
            $.get(endpoint).then(setstate_cb);
            setTimeout(cb, timeout_ms);
        };
        cb();
    }

	render() {
        let objs = [];
        Object.entries(this.state).forEach(([key, value]) => {
            objs.push(key + "=" + JSON.stringify(value));
        });
		return (
            <>
            REACT STUFF :D
            <ul> { objs.map((idx, i) => <li key={i}> {idx} </li>) } </ul>
            </>
		);
	}
};

export default App;
