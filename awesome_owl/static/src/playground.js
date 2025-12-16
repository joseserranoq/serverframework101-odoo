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
        this.todos = useState([
            {id: 1, description: "Buy groceries", isCompleted: false},
            {id: 2, description: "Walk the dog", isCompleted: true},
            {id: 3, description: "Read a book", isCompleted: false},
        ]);
    }
    onChange() {
        this.sum.value++;
    }
}