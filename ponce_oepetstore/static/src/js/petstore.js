
openerp.oepetstore = function(instance) {
    var _t = instance.web._t,
        _lt = instance.web._lt;
    var QWeb = instance.web.qweb;

    instance.oepetstore = {};

    instance.oepetstore.HomePage = instance.web.Widget.extend({
        start: function() {
            console.log("pet store home page loaded");
        },
    });
    
    instance.web.client_actions.add('petstore.homepage', 'instance.oepetstore.HomePage');

    instance.oepetstore.MyClass = instance.web.Class.extend({
    say_hello: function() {
    console.log("hello");
    },
    });
    var my_object = new instance.oepetstore.MyClass();
    my_object.say_hello();
}