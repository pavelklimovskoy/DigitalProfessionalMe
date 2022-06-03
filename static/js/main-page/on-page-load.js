// Действия при открытии страницы
window.onload = function () {
    loadSkills();


    createTimeline();
}

document.querySelector("#close").addEventListener("click", function(){
    document.querySelector(".popup").style.display = "none";
});