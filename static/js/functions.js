function signUp() {
  var login = document.getElementById("login");
  var signUp = document.getElementById("sign-up");
    login.style.display = "none";
    signUp.style.display = "block";
}

function logIn() {
  var login = document.getElementById("login");
  var signUp = document.getElementById("sign-up");
    signUp.style.display = "none";
    login.style.display = "block";
}


// PROGRESS BAR DOUNUT


var myWidgetInstances = {} 
// Wrap your original code inside a function that recieves a newClassName parameter.
var createInstance = function(newClassName, index) {
    var Gradient = '<defs><linearGradient id="gradient" x1="10%" y1="25%" x2="100%" y2="20%" gradientUnits="userSpaceOnUse"><stop offset="0%" stop-color="#11C684"/><stop offset="100%" stop-color="#4963FE"/><stop offset="30%" stop-color="#4963FE"/></linearGradient></defs>';
    var form_progress = new ProgressBar.Circle('.' + newClassName, { // <-- Reference the new class name.
      strokeWidth: 10,
      color: 'url(#gradient)',
      trailColor: '#fff',
      trailWidth: 10,
      easing: 'easeInOut',
      duration: 1400,
      svgStyle: null,
      text: {
        value: '',
        alignToBottom: false
      },
  
  
      // Set default step function for all animate calls
      step: (state, bar) => {
        var value = Math.round(bar.value() * 100);
        bar.setText('<p class="progress-bar-title">Rate</p>'+value);
        // if (value === 0) {
        //   bar.setText('');
        // } else {
        //   bar.setText('<p class="progress-bar-title">Rate</p>'+value+"<span>%</span>");
        // }
  
        bar.text.style.color = state.color;
        bar.svg.insertAdjacentHTML('afterbegin', Gradient);
        bar.text.style.fontFamily = '"Open Sans", sans-serif';
      }
      
    });
    // Add this instance to a myWidgetInstances object so it can be referenced later;
    myWidgetInstances['form_progress-' + index] = form_progress;
    
}

// Obtain a reference to all the DOM elements with a classname '.form-progress'.
var all_instances = [].slice.call(document.querySelectorAll('.progress-bar-donut'));
let progress_bar_counts = document.querySelectorAll('.progressbar-text').length;
// console.log(progress_bar_counts)
// window.alert(progress_bar_counts.length)
// Loop through each instance of a DOM element with a classname '.form-progress'
all_instances.forEach(function(element, index, dataset) {

    // Create a new classname. The same as before except
    // with a number suffix.
    index = index + progress_bar_counts;
    var newClassName = 'form-progress-' + index;
    

    // Add the new classname to the DOM element.
    element.classList.add(newClassName);
    
    

    // Invoke the createInstance function passing
    // the 'newClassName' as an argument.
    createInstance(newClassName, index);
    var x = element.getAttribute("data-prograss");
    myWidgetInstances['form_progress-' + index].animate(x);
});


// PROGRESS BAR LINE

//
// linear-gradient(90deg, #6295FF 0%, #8C19E5 100%)
//


var myWidgetInstances = {} 
// Wrap your original code inside a function that recieves a newClassName parameter.
var GradientG = '<defs><linearGradient id="gradient" x1="10%" y1="25%" x2="100%" y2="20%" gradientUnits="userSpaceOnUse"><stop offset="0%" stop-color="#11C684"/><stop offset="100%" stop-color="#4963FE"/><stop offset="30%" stop-color="#4963FE"/></linearGradient></defs>';
var GradientB = '<defs><linearGradient id="blue" x1="10%" y1="25%" x2="100%" y2="20%" gradientUnits="userSpaceOnUse"><stop offset="0%" stop-color="#6295FF"/><stop offset="100%" stop-color="#8C19E5"/><stop offset="30%" stop-color="#4963FE"/></linearGradient></defs>';
var createInstance = function(newClassName, index) {
    var form_progress = new ProgressBar.Line('.' + newClassName, { // <-- Reference the new class name.
      strokeWidth: 2,
      color: 'url(#blue)',
      trailColor: '#fff',
      trailWidth: 2,
      easing: 'easeInOut',
      duration: 1400,
      svgStyle: null,
      text: {
        value: '',
        alignToBottom: true
      },
  
  
      // Set default step function for all animate calls
      step: (state, bar) => {
        var value = Math.round(bar.value() * 100);
        if (value === 0) {
          bar.setText('');
        } else {
          bar.setText('<span>'+value+'%</span>');
        }
  
        bar.text.style.color = state.color;
        bar.svg.insertAdjacentHTML('afterbegin', GradientB);
        bar.text.style.fontFamily = '"Open Sans", sans-serif';
      }
      
    });
    // Add this instance to a myWidgetInstances object so it can be referenced later;
    myWidgetInstances['form_progress-' + index] = form_progress;
    
}

// Obtain a reference to all the DOM elements with a classname '.form-progress'.
var all_instances = [].slice.call(document.querySelectorAll('.progress-bar-line'));
progress_bar_counts = document.querySelectorAll('.progressbar-text').length
// console.log(progress_bar_counts)
// window.alert(progress_bar_counts.length)
// Loop through each instance of a DOM element with a classname '.form-progress'
all_instances.forEach(function(element, index) {

    // Create a new classname. The same as before except
    // with a number suffix.
    index = index + progress_bar_counts;
    var newClassName = 'form-progress-' + index;
    

    // Add the new classname to the DOM element.
    element.classList.add(newClassName);
    
    

    // Invoke the createInstance function passing
    // the 'newClassName' as an argument.
    createInstance(newClassName, index);
    var x = element.getAttribute("data-prograss");
    var a = element.getAttribute("data-color");
    var b = element.children;
    console.log(b);
    myWidgetInstances['form_progress-' + index].animate(x);
});

// The following assumes there are atleast three 
// html div tags as follows:
// 
// <div class="form-progress"></div>



// SWITCHER

function uploadList(data) {
  var switcher = data.getAttribute("data-target");
  var target = document.querySelector(""+switcher);
  if( target.disabled == false)
    {
      target.disabled = true;
    }
    else
    {
      target.disabled = false;
    }
}

// SIDEBAR NAV TOGGLE

function navToggle() {

  var logoWrapper = document.getElementsByClassName('logo-wrapper');
  var sideNavbar = document.getElementsByClassName('side__navbar-wrapper');
  var content = document.querySelectorAll('.plat-content > .content');

  sideNavbar[0].classList.toggle("toggle-on");
  logoWrapper[0].classList.toggle("toggle-on");
  content[0].classList.toggle("navbarToggled");

}

