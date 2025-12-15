import { whenReady } from "@odoo/owl";
import { mountComponent } from "@web/env";
import { Playground } from "./playground";

const config = {
    dev: true,
    name: "Owl Tutorial",
    // we need to write the props here because we are not using
    // the <Playground/> tag in an XML template
    props: {title : 'title', content : 'content'},
};

// Mount the Playground component when the document.body is ready
whenReady(() => mountComponent(Playground, document.body, config));

