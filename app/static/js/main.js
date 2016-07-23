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

  var LeafScene = function(el) {
    this.viewport = el;
    this.world = document.createElement('div');
    this.leaves = [];

    this.width = this.world.offsetWidth;
    this.height = this.world.offsetHeight;

    this.options = {
      numLeaves: 30,
      windspeed: 0.2
    };
  }

  LeafScene.prototype.init = function() {
    for (var i = 0; i < this.numLeaves; i++) {
      var leaf = var leaf = {
        el: document.createElement('div'),
        x: Math.random()*this.width,
        y: Math.random()*this.height/2,
        rX: 0,
        rY: 0,
        rZ: 0,
        xSpeed: 0,
        ySpeed: 0,
        rSpeed: 0,
        pathType: 1
      };
      this.leaves.push(leaf);
      this.world.appendChild(leaf.el);
    }

    this.world.className = 'leaf-scene';
    this.viewport.appendChild(this.world);
  }

  LeafScene.prototype.resetLeaf = function(leaf) {
    var x, y, r, rSpeed;

    // start offscreen, within a third of the top right corner
    x = Math.random()*this.width*2/3 + (this.width*2/3);
    y = -10;
    if (x > this.width) {
      x = this.width + 10;
      y = Math.random()*this.height/3;
    }

    // rotate around the y or z axis
    r = 0;
    rSpeed = Math.random()*0.1;

    return leaf;
  }


})();