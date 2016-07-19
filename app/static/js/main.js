(function() {
  'use strict';

  FastClick.attach(document.body);

  // helper fn to get parent
  function get_parent(el, className, context) {
    while ( el && !el.classList.contains(className) ) {
      el = el.parentNode;

      if ( el === context ) return false;
    }
    return el;
  }

})();