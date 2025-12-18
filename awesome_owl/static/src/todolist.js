import { Component, useState } from "@odoo/owl";
export class TodoList extends Component {
    static template = "awesome_owl.todolist";
    static props = ["todos"];
    setup() {
        this.todos = useState([]);
    }
    addTodo(e) {
        e.preventDefault();
        console.log('Key pressed:', e.target.value, e.keyCode);
        if (e.keyCode === 13 && e.target.value.trim() !== "") {
            const newTodo = {
                id: this.props.todos.length + 1,
                description: e.target.value,
                isCompleted: false,
            };
            this.props.todos.push(newTodo);
            e.target.value = "";
        }
        console.log('Current todos:', this.props.todos);

    }
    

}