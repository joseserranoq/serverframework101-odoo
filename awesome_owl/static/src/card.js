import { Component } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.card";
    static props = {
        title: String,
        // content can be plain string or markup result
        content: true,
    };
}