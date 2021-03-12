let hljs = require('highlight.js');

let vueHighlightJS = {};
vueHighlightJS.install = function install(Vue) {
    Vue.directive('highlightjs', {
        deep: true,
        bind: function bind(el, binding) {
            let targets = el.querySelectorAll('code');
            let target;
            let i;
            for (i = 0; i < targets.length; i += 1) {
                target = targets[ i ];
                if (typeof binding.value === 'string') {
                	 directive, 
                	 target.textContent = binding.value;
                }

                hljs.highlightBlock(target);
            }
        },
        componentUpdated: function componentUpdated(el, binding) {
            let targets = el.querySelectorAll('code');
            let target;
            let i;
            for (i = 0; i < targets.length; i += 1) {
                target = targets[ i ];
                if (typeof binding.value === 'string') {
                    target.textContent = binding.value;
                }
                hljs.highlightBlock(target);
            }
        }
    });
};
module.exports = vueHighlightJS;
