import { Component, useState } from "@odoo/owl";
export class TodoList extends Component {
    static template = "awesome_owl.todolist";
    static props = ["todos"];
    setup() {
        //this.todos = useState([]);
    }
    addTodo(e) {
        e.preventDefault();
        console.log('Key pressed:', e.target.value, e.keyCode);
        if(e.keyCode === 13) {
            const newTodo = {
                id: this.todos.length + 1,
                description: e.target.value,
                isCompleted: false,
            };
            this.todos.push(newTodo);
            e.target.value = "";
        }        
    }

}