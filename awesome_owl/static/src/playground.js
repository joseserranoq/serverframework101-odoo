import { Component, useState, markup } from "@odoo/owl";
import { Counter } from "./counter";
import { Card } from "./card";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card };

    setup() {
        this.count = useState({ value: 0 });
        // plain string → escaped by t-out
        this.content1 = "<div class='text-primary'>some content</div>";
        // markup() → rendered as HTML by t-out
        this.content2 = markup("<div class='text-primary'>some content</div>");

        this.title1 = "card 1";
        this.title2 = "card 2";
    }

    increment() {
        this.count.value++;
    }
}