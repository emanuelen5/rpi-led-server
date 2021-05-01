import React, { Component } from "react";
import $ from 'jquery';
import { Manager } from "socket.io-client";

const manager = new Manager("ws://" + window.location.host + "/api/socketio", {
    path: "/api/socketio",
    reconnectionDelayMax: 10000,
    query: {
        "my-key": "my-value"
    },
});

const socket = manager.socket("/test", {
    auth: {
        token: "123"
    }
});
socket.on("connect", () => {
    console.log("Connected with id: " + socket.id);
});
socket.on("reconnect", () => {
    console.log("Reconnected");
});

class App extends Component {
    constructor(props) {
        super(props);
        this.state = {
        };
        this.update = this.update.bind(this);
        //this.update("/api/display", 200);
        //this.update("/api/settings", 500);
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
