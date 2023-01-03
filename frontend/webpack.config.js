var webpack = require('webpack');
var path = require('path');

var BUILD_DIR = path.resolve(__dirname, '..', 'static', 'js');
var APP_DIR = path.resolve(__dirname, 'app');

var config = {
  mode: "development",
  devtool: 'inline-sourcemap',
  entry: [APP_DIR + '/index.jsx'],
  output: {
    path: BUILD_DIR,
    filename: 'myapp.js'
  },
  module : {
    rules : [
      {
        test : /\.jsx?/,
        include : APP_DIR,
        loader : 'babel-loader',
        query: {
          presets: ['@babel/react', '@babel/preset-env'],
          plugins: ['react-html-attrs', 'transform-class-properties'],
        }
      }
    ]
  },
  plugins: [
     new webpack.DefinePlugin({
      'process.env': {
        'NODE_ENV': JSON.stringify('development')
      }
    })
  ]
};

module.exports = config;
