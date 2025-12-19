import { Component, useState,useRef } from "@odoo/owl";
export class TodoList extends Component {
    static template = "awesome_owl.todolist";
    static props = ["todos"];
    setup() {
        //this.todos = useState([]);
        this.myRef = useRef("todo-input");
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
    }
    toggleState(id) {
        const todo = this.props.todos.find(t => t.id === id);
        if (todo) {
            todo.isCompleted = !todo.isCompleted;
            console.log('Updated todos list:', this.props.todos);
        }
    }
    removeTodo(id) {
        const index = this.props.todos.findIndex(t => t.id === id);
        if (index !== -1) {
            this.props.todos.splice(index, 1);
            console.log('Updated todos list after removal:', this.props.todos);
        }
    }
}