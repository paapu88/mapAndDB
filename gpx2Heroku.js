/*
https://stackoverflow.com/questions/43710706/converting-jquery-to-pure-javascript-on-submit-form
*/

function makeAjaxRequest(url, method, data) {
    var xhr;
    xhr = new XMLHttpRequest();
    //console.log("starting httprequest: " +data)
    if (!xhr) {
        console.log('Giving up :( Cannot create an XMLHTTP instance');
        return false;
    }

    xhr.open(method, url, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    //console.log("SENDING:"+data)
    xhr.send(data);

    xhr.onreadystatechange = (function () {
      //console.log("state change")
        if (xhr.readyState == 4 && xhr.status == 200){
          console.log(xhr.responseText)
        }else{
          console.log(xhr.responseText+ " "+xhr.status)
        }
    });

}



(function(){
    document.addEventListener('DOMContentLoaded',function(){
        var form = document.querySelector('form');
        form.addEventListener('submit',function(e){
            e.preventDefault();
            //var login = document.getElementById("login").value;
            var tag = document.getElementById("tag").value;

            var mail = document.getElementById("mail").value;
            var coord = document.getElementById("coord").value;
            coord = coord.replace(/(\r\n\t|\n|\r\t)/gm,"");

            if(tag === '' || mail === '') {
                alert('Les champs doivent êtres remplis');
            } else {
                // var form = document.querySelector('form');
                //   var data = new FormData(form);
                var today = new Date();
                var dd = today.getDate();
                var mm = today.getMonth() + 1; //January is 0!
                var yyyy = today.getFullYear();
                if (dd < 10) {
                  dd = '0' + dd;
                }
                if (mm < 10) {
                  mm = '0' + mm;
                }
                var now = yyyy.toString() + mm.toString() + dd.toString();
                //console.log("coord:"+coord)
                //console.log("now:"+yyyy)
                //console.log("now:"+mm)
                //console.log("now:"+dd)

                var url = "https://map-and-db.herokuapp.com/track/"+tag
                var method = "POST"
                var data = JSON.stringify({"date": now, "track": coord})
                //console.log("url:"+url)
                //console.log("data:"+data)
                makeAjaxRequest(url,method,data);
            }
        });

    });
})();

/*
{'date': '20181225',
'track': '60.149550279193875 24.75560806319329 60.14931547128022 24.80439491132073 60.15198472458916 24.819419235886798
60.152194190084955 24.83861947675856 60.14743070817223 24.8499100577668 60.13103262171181 24.897190511471724
60.12797582699717 24.8640499193377 60.13046472630084 24.835825111157835 60.132792361054506 24.8173134629918
60.12878151068023 24.772425934717894 60.137421055774404 24.77289688966289 60.14464429205473 24.758053503576615
60.148001720060314 24.757402617572478'}


*/
