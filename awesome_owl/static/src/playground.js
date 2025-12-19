import { Component, useState, markup } from "@odoo/owl";
import { Counter } from "./counter";
import { Card } from "./card";
import { TodoList } from "./todolist";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card, TodoList };

    setup() {
        this.sum = useState({ value: 0 });
        // to bind it needs a function in the father compoonent 
        // and also the line of code below
        // or we can use callback.bind in the XML 
        // in this case onChange.bind="onChange"
        // this.onChange = this.onChange.bind(this);
        // plain string → escaped by t-out
        this.content1 = "<div class='text-primary'>some content</div>";
        // markup() → rendered as HTML by t-out
        this.content2 = markup("<div class='text-primary'>some content</div>");
        this.title1 = "card 1";
        this.title2 = "card 2";
        this.todos = useState([]);
        //this.toggleState = this.toggleState.bind(this);
    }
    onChange() {
        this.sum.value++;
    }
    toggleState(id) {
        const todo = this.todos.find(t => t.id === id);
        if (todo) {
            todo.isCompleted = !todo.isCompleted;
            console.log('Updated todos list:', this.todos);
        }
    }
}