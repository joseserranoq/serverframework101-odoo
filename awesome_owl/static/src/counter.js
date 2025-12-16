import { Component, useState } from "@odoo/owl";

export class Counter extends Component {
    static template = "awesome_owl.counter";
    static props = ['onChange?'];
    setup() {
        this.count = useState({ value: 0 });
        this.sum = useState({ value: 0 });
        this.todos = useState([
            {id: 1, description: "Buy groceries", isCompleted: false},
            {id: 2, description: "Walk the dog", isCompleted: true},
            {id: 3, description: "Read a book", isCompleted: false},
        ]);
    }

    increment() {
        this.count.value++;
        if (this.props.onChange) {
            this.props.onChange();
            console.log('onChange called from Counter');
        }
    }
}
