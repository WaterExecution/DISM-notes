function find() {
    var query = document.getElementById("search").value;
    var searchArr = document.getElementsByClassName('searchMe');
    if (query != "") {
        for (i = 0; i < searchArr.length; i++) {
            var reset = searchArr[i].innerHTML.replaceAll("<span>", "");
            reset = reset.replaceAll("<\/span>", "");
            searchArr[i].innerHTML = reset;
            var RegExquery = new RegExp("(\\b" + query + "\\b)", "gim");
            var e = searchArr[i].innerHTML;
            var newe = e.replace(RegExquery, "<span>$&</span>");
            searchArr[i].innerHTML = newe;
        }
    } else {
        for (i = 0; i < searchArr.length; i++) {
            var reset = searchArr[i].innerHTML.replaceAll("<span>", "");
            reset = reset.replaceAll("<\/span>", "");
            searchArr[i].innerHTML = reset;
        }
    }
}