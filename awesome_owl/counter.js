odoo.define('@awesome_owl/counter', ['@odoo/owl'], function (require) {
    const { Component, useState } = require('@odoo/owl');

    class Counter extends Component {
        static template = "awesome_owl.counter";

        setup() {
            this.count = useState({ value: 0 });
        }
        increment() {
            this.count.value++;
        }
    }

    return { Counter };
});
