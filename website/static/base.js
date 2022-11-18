var app = angular.module("App", []);
app.filter('jsonDate', ['$filter', function ($filter) {
    return function (input, format) {
        return (input)
            ? $filter('date')(parseInt(input.substr(6)), format)
            : '';
    };
}]);
app.controller("Base", ["$scope", "$window", "$http", "$filter", function ($scope, $window, $http, $filter) {
    $scope.convert_choice = 1;
    $scope.convert_quality = "low";
    $scope.UrlTo = function(choice){
        $scope.convert_choice = choice;
        if(choice==1){
            document.getElementById('quality-tab').style = "display:visible";
        }
        else{
            document.getElementById('quality-tab').style = "display:none";
        }
    }
    $scope.Quality = function(quality){
        $scope.convert_quality = quality
    }
    $scope.youtube_downloader = function(){
        document.getElementById('conn').style.visibility = "visible";
        document.getElementById('hh').className= "modal-backdrop fade show";
        $scope.links = $scope.link.split(",");
        console.log($scope.link)
        console.log($scope.links)
        $scope.model = {
            choice:$scope.convert_choice,
            quality:$scope.convert_quality,
            link:$scope.link,
            links:$scope.links
        }
        console.dir($scope.model)
        $http({
            method: 'POST',
            url: "/youtube_downloader",
            data: JSON.stringify($scope.model),
            dataType: "json"
        }).then(function (d) {
            console.log(d.data);
            if(d.data.result=="0"){
                alertify.error("Youtube video url manzili kiritilmagan");
                document.getElementById('hh').className= "fade hide";
                document.getElementById('conn').style.visibility = "hidden";
            }
            else{
                window.location.href = "/send_file?filename="+d.data.result;
                setTimeout(function() {
                    $http({
                        method: 'POST',
                        url: "/remove_file?filename="+d.data.result,
                    }).then(function (d) {
                        console.log(d.data);
                        document.getElementById('hh').className= "fade hide";
                        document.getElementById('conn').style.visibility = "hidden";
                    }, function (error) {
                        document.getElementById('hh').className= "fade hide";
                        document.getElementById('conn').style.visibility = "hidden";
                        console.log("error in remove_file -> ", error);
                    });
                }, 3000);
                alertify.success("Fayl yuklanmoqda...");
            }
        }, function (error) {
            alertify.error("Xatolik yuz berdi");
            document.getElementById('hh').className= "fade hide";
            document.getElementById('conn').style.visibility = "hidden";
            console.log("error in youtube_downloader -> ", error);
        });
    }
    $scope.instagram_downloader = function(){
            document.getElementById('conn').style.visibility = "visible";
            document.getElementById('hh').className= "modal-backdrop fade show";
            $scope.model = {
                user_name:$scope.instagram_user_name
            }
            console.dir($scope.model)
            $http({
                method: 'POST',
                url: "/instagram_downloader",
                data: JSON.stringify($scope.model),
                dataType: "json"
            }).then(function (d) {
                console.log(d.data);
                if(d.data.result=="0"){
                    alertify.error("Instagram profil nomi kiritilmagan");
                    document.getElementById('hh').className= "fade hide";
                    document.getElementById('conn').style.visibility = "hidden";
                }
                else{
                    window.location.href = "/send_file?filename="+d.data.result;
                    setTimeout(function() {
                        $http({
                            method: 'POST',
                            url: "/remove_file?filename="+d.data.result,
                        }).then(function (d) {
                            console.log(d.data);
                            document.getElementById('hh').className= "fade hide";
                            document.getElementById('conn').style.visibility = "hidden";
                        }, function (error) {
                            document.getElementById('hh').className= "fade hide";
                            document.getElementById('conn').style.visibility = "hidden";
                            console.log("error in remove_file -> ", error);
                        });
                    }, 3000);
                    alertify.success("Fayl yuklanmoqda...");
                }
            }, function (error) {
                alertify.error("Xatolik yuz berdi");
                document.getElementById('hh').className= "fade hide";
                document.getElementById('conn').style.visibility = "hidden";
                console.log("error in instagram_downloader -> ", error);
            });
        }
    $scope.login="Login";
    $scope.clickLogin = function(){
        myModal.show();
    }
    $scope.user=checkAuth();
    if($scope.user!=false){
        $scope.login=checkUserName();
    }
    function getContacts(){
            $http({
                method: 'POST',
                url: "/getUser?uid="+$scope.user.uid+"&not_me=1",
            }).then(function (d) {
                console.log(d.data);
                $scope.Contacts = d.data;
            }, function (error) {
                console.log("error in getUser -> ", error);
            });
    }
    function getChatUserRelations(){
            $http({
                method: 'POST',
                url: "/getChatUserRelations?user_id="+$scope.user.id,
            }).then(function (d) {
                console.log(d.data);
                $scope.ChatUserRelations = d.data;
            }, function (error) {
                console.log("error in getChatUserRelations -> ", error);
            });
    }
    function getMyContacts(){
            $http({
                method: 'POST',
                url: "/getMyContacts?user_id="+$scope.user.id,
            }).then(function (d) {
                console.log(d.data);
                $scope.MyContacts = d.data;
            }, function (error) {
                console.log("error in getMyContacts -> ", error);
            });
    }
    $scope.loadContacts = function(){
        getMyContacts()
    }
    $scope.loadChats = function(){
        getChatUserRelations()
    }
    function loadMessageByContactId(receiver_id){
        $http({
            method: 'POST',
            url: "/getChatMessages?receiver_id="+receiver_id+"&sender_id="+$scope.user.id,
        }).then(function (d) {
            console.log(d.data);
            $scope.Messages = d.data;
        }, function (error) {
            console.log("error in getChatMessages -> ", error);
        });
    }
    $scope.loadMessageByContactId = function(receiver_id, index, count){
        $scope.is_chat=0
        $scope.is_contact=1
        $scope.receiver_id=receiver_id
        for(i=0;i<count;i++){
           document.getElementById("contact"+i).className = "friend-drawer--onhover";
        }
        document.getElementById("contact"+index).className = "active";
        $scope.selectedUser=$scope.MyContacts.filter(user => user.id == receiver_id)[0]
        console.log($scope.selectedUser)
        document.getElementById('contactsArea').style.display = "none"
        document.getElementById('messageTextArea').style.display = "block"
        $(".chat-bubble").hide("slow").show("slow");
        loadMessageByContactId(receiver_id)
    }
    var socket;
    $(document).ready(function(){

    });
    socket = io.connect('http://' + document.domain + ':' + location.port + '/chat');
    socket.on('connect', function() {
        socket.emit('join', {});
    });
    socket.on('status', function(data) {
        if(data.active){
            alertify.success(data.text);
        }
        else{
            alertify.error(data.text);
        }
    });
    socket.on('message', function(data) {
        console.log($scope.Messages)
        console.log(data)
//            $('#chat').val($('#chat').val() + data.text + '\n');
//            $('#chat').scrollTop($('#chat')[0].scrollHeight);
    });
    $('#send').click(function(e) {
        text = $('#text').val();
        $('#text').val('');
        socket.emit('text', {msg: text});
    });
    $window.join_room = function() {
        myModal.hide();
        socket.emit('join', {});
    };
    $window.leave_room = function() {
        myModal.hide();
        socket.emit('left', {});
    };
    $scope.openForm = function() {
        if($scope.login=="Login"){
            myModal.show();
//            window.location.href = "/login"
        }
        else{
            if($scope.MyContacts==null){
                getMyContacts()
            }
            for(i=0;i<document.getElementsByClassName('friend-drawer selected_user').length;i++){
               document.getElementsByClassName('friend-drawer selected_user')[i].className = "friend-drawer friend-drawer--onhover";
            }
            document.getElementById("myForm").style.display = "block";
            document.getElementById("openChatBtn").style.display = "none";
        }
    }
    $scope.closeForm = function() {
	  document.getElementById("myForm").style.display = "none";
	  document.getElementById("openChatBtn").style.display = "block";
	}
	$scope.closeMessageArea = function(){
	    document.getElementById('messageTextArea').style.display = "none"
        document.getElementById('contactsArea').style.display = "block"

	}
    function loadMessageByChatId(chat_id){
        $http({
            method: 'POST',
            url: "/getChatMessagesByChatId?chat_id="+chat_id,
        }).then(function (d) {
            console.log(d.data);
            $scope.Messages = d.data;
        }, function (error) {
            console.log("error in getChatMessagesByChatId -> ", error);
        });
    }
    $scope.loadMessageByChatId = function(receiver_id, chat_id, index, count){
        $scope.is_chat=1
        $scope.is_contact=0
        $scope.receiver_id=receiver_id
        for(i=0;i<count;i++){
           document.getElementById("user"+i).className = "friend-drawer friend-drawer--onhover";
        }
        document.getElementById("user"+index).className = "friend-drawer selected_user";
        $scope.selectedUser=$scope.ChatUserRelations.filter(user => user.user_id == receiver_id)[0].user
        console.log($scope.selectedUser)
        document.getElementById('messageTextArea').style.display = "block"
        $(".chat-bubble").hide("slow").show("slow");
        loadMessageByChatId(chat_id)
    }
    $scope.sendMessage=function(){
        $scope.model={
            sender_id:$scope.user.id,
            receiver_id:$scope.receiver_id,
            text:$scope.text
        }
        console.log($scope.model)
        $http({
            method: 'POST',
            url: "/sendMessage",
            data: JSON.stringify($scope.model),
            dataType: "json"
        }).then(function (d) {
            console.log(d.data);
            $scope.text=''
//            if($scope.is_chat==1){
//                loadMessageByChatId(d.data[0].chat_id)
//            }
//            if($scope.is_contact==1){
//                loadMessageByContactId($scope.receiver_id)
//            }
        }, function (error) {
            console.log("error in sendMessage -> ", error);
        });
    }

}]);