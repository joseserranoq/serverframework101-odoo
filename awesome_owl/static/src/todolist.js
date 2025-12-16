import { Component, useState } from "@odoo/owl";
export class TodoList extends Component {
    static template = "awesome_owl.todolist";
    static props = ["todos"];
}