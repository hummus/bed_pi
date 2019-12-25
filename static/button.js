

function move(movement_name) {

  var xhr = new XMLHttpRequest();
  xhr.open('GET', '../bed_recline_movement_pulse/' + movement_name);
  xhr.send();

  xhr.onreadystatechange = function () {
    var DONE = 4; // readyState 4 means the request is done.
    var OK = 200; // status 200 is a successful return.
    if (xhr.readyState === DONE) {
      if (xhr.status === OK) {
        console.log(xhr.responseText); // 'This is the returned text.'
      } else {
        console.log('Error: ' + xhr.status); // An error occurred during the request.
      }
    }
  };
}



function holdit(button, action) {
  var t;

  var repeat = function () {
    move(button.value);
    t = setTimeout(repeat, 500);
  }

  button.addEventListener('mousedown', e => {
    console.log('mousedown');
    repeat();
  });

  button.addEventListener('mouseup', e => {
    console.log('mouseup');
    clearTimeout(t);
  });
};

window.addEventListener('load', function() {

  const button = document.getElementById("top-up");

  holdit(button, function() {
    console.log('sent request');
  });  

});
