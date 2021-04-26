import React from 'react';
import ReactDOM from 'react-dom';
import StorageItem from "./storage"

import $ from 'jquery';
import 'bootstrap';

require('../static/index.html');
import App from './app';

const STORAGE_CONFIG = 'config';

const config = new StorageItem(STORAGE_CONFIG, {is_initialized: false});

ReactDOM.render(
    <App config={config} />,
    document.getElementById('app')
);
