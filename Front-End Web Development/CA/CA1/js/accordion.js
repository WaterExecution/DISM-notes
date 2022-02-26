function ready(){
 var acc = document.getElementsByClassName("accordionList");
 var i;
 for (i = 0; i < acc.length; i++) {
  acc[i].addEventListener("click", function() {
   this.classList.toggle("active");
   var panel = this.nextElementSibling;
   if (panel.style.maxHeight) {
    panel.style.maxHeight = null;
    panel.style.padding = "0";
    panel.style.border = null;
   } else {
    panel.style.maxHeight = panel.scrollHeight + "px";
    panel.style.padding = "0 0 10px 18px";
    panel.style.border = "5px solid var(--secondary-color)";
   } 
  });
 }
}

window.addEventListener('DOMContentLoaded', ready);