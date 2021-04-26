const webpack = require('webpack');
const { merge } = require('webpack-merge');
const common = require('./webpack.common.js');

module.exports = merge(common, {
    mode: "development",
    devtool: false,
    devServer: {
        contentBase: './.build',
    },
    plugins: [
        new webpack.EvalSourceMapDevToolPlugin({
            filename: '[name].[ext].map',
            exclude: [
                /node_modules/
            ]
        })
    ],
});
