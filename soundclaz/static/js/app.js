        // Wrap every letter in a span
        let textWrapper = document.querySelector('.ml3');
        textWrapper.innerHTML = textWrapper.textContent.replace(/\S/g, "<span class='letter'>$&</span>");
        anime.timeline({loop: true})
          .add({
            targets: '.ml3 .letter',
            opacity: [0,1],
            easing: "easeInOutQuad",
            duration: 1000,
            delay: (el, i) => 150 * (i+1)
          }).add({
            targets: '.ml3',
            opacity: 0,
            duration: 1000,
            easing: "easeOutExpo",
            delay: 1000
          });

          //SHARE CODE
// const linkedinBtn = document.querySelector(".linkedin-btn");

// function init(){
//     let postUrl = encodeURI(document.location.href);
//     let postTitle = encodeURI("Hi everyone, please check this out: ");
    

//     linkedinBtn.setAttribute(
//         "href",
//         `https://www.linkedin.com/shareArticle?url=${postUrl}&title=${postTitle}`
//     );
//   }
//   init();

//END OF SHARE CODE