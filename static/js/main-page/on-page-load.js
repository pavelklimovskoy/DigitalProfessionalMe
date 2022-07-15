// Действия при открытии страницы
window.onload = function () {
    loadSkills();

    let cookieId = document.cookie.match('(^|;)\\s*' + 'id' + '\\s*=\\s*([^;]+)')?.pop() || '';
    
    
    //alert("id from BD of the currently logged in user is: " + cookieId);
    
    createTimeline();
}

//document.querySelector("#close").addEventListener("click", function(){
//    document.querySelector(".popup").style.display = "none";
//});