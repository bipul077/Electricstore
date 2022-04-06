function myFunction(x) {
    if (x.matches) { // If media query matches
        $('.owl-carousel').owlCarousel({
            loop:true,
            margin: 20,
            nav:false,
            dots:false,
            autoplay: false,
            autoplayTimeout: 1000,
            stagePadding: 30,
            responsive:{
                0:{
                    items:1
                },
                600:{
                    items:3
                },
                1000:{
                    items:4
                }
            }
        }) 
    } else {
        $('.owl-carousel').owlCarousel({
            loop:true,
            margin: 20,
            nav:false,
            dots:false,
            autoplay: false,
            autoplayTimeout: 1000,
            stagePadding: 50,
            responsive:{
                0:{
                    items:1
                },
                600:{
                    items:3
                },
                1000:{
                    items:5
                }
            }
        })
    }
  }
  
  var x = window.matchMedia("(max-width: 700px)")
  myFunction(x) // Call listener function at run time
  x.addListener(myFunction) // Attach listener function on state changes