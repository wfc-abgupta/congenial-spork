import React from "react"
import ReactDOM from "react-dom"
import { Provider } from "react-redux"
import { applyMiddleware, createStore } from "redux"
import thunk from "redux-thunk"
import "idempotent-babel-polyfill"

import { reducer } from "./stores"

const store = createStore(reducer, applyMiddleware(thunk))

const MyApp = () => (
    <Provider store={store}>
		// insert your component here
    </Provider>
)

ReactDOM.render(MyApp(), document.getElementById("app"))
