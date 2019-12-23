
function var oReq = new XMLHttpRequest();
oReq.onload = function (e) {
    results.innerHTML = e.target.response.message;
};
oReq.open('GET', e.target.dataset.url + '?' + new Date().getTime(), true);
oReq.responseType = 'json';
oReq.send();


function holdit(button, action) {
  var t;

  var repeat = function () {
    action();
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
