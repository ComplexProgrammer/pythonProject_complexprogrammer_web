function setCookie(cname, cvalue, exdays) {
    alert(cname)
    alert(cvalue)
    alert(exdays)
    const d = new Date();
    d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
    let expires = "expires="+d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

function removeCookie(cname){
    document.cookie = cname + "= ; expires = Thu, 01 Jan 1970 00:00:00 GMT";
}

function getCookie(cname) {
    let name = cname + "=";
    let ca = document.cookie.split(';');
    for(let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

function checkAuth(){
    if(getCookie("user")){
        var user = JSON.parse(getCookie("user"));
        console.log(user);
        return user;
    }
    else{
        return false;
    }
}
function checkUserName(){
    if(getCookie("user")){
        var user = JSON.parse(getCookie("user"));
        console.log(user)
        var name='';
        if(user.name)
            name=user.name;
        else
            if(user.email)
                name=user.email;
            else
                if(user.phone)
                    name=user.phone;

        return name;
    }
    else{
        return false;
    }
}
