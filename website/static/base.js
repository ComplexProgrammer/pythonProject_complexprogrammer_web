var app = angular.module("App", []);
app.filter('jsonDate', ['$filter', function ($filter) {
    return function (input, format) {
        return (input)
            ? $filter('date')(parseInt(input.substr(6)), format)
            : '';
    };
}]);
app.controller("Base", ["$scope", "$http", "$filter", function ($scope, $http, $filter) {
    $scope.login="Login";
    $scope.user=checkAuth();
    $scope.user_name=checkUserName();
    if($scope.user!=false){
        $scope.user_id=$scope.user.id;
        $scope.photo_url=$scope.user.photo_url;
        $scope.name=$scope.user.name;
        $scope.email=$scope.user.email;
        $scope.phone=$scope.user.phone;
        $scope.provider_id=$scope.user.provider_id;
        $scope.uid=$scope.user.uid;
        $scope.user_active=$scope.user.active;
        if($scope.user.name)
            $scope.login=$scope.user.name;
        else
            if($scope.user.email)
                $scope.login=$scope.user.email;
            else
                if($scope.user.phone)
                    $scope.login=$scope.user.phone;
    }
    function getContacts(){
            $http({
                method: 'POST',
                url: "/getUser?uid="+$scope.uid+"&not_me=1",
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
                url: "/getChatUserRelations?user_id="+$scope.user_id,
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
                url: "/getMyContacts?user_id="+$scope.user_id,
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
            url: "/getChatMessages?receiver_id="+receiver_id+"&sender_id="+$scope.user_id,
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
           document.getElementById("contact"+i).className = "friend-drawer friend-drawer--onhover";
        }
        document.getElementById("contact"+index).className = "friend-drawer selected_user";
        $scope.selectedUser=$scope.MyContacts.filter(user => user.id == contact_id)[0]
        console.log($scope.selectedUser)
        document.getElementById('messageTextArea').style.display = "block"
        $(".chat-bubble").hide("slow").show("slow");
        loadMessageByContactId(receiver_id)
    }
    $scope.openForm = function() {
        if($scope.ChatUserRelations==null){
            getChatUserRelations()
        }
        for(i=0;i<document.getElementsByClassName('friend-drawer selected_user').length;i++){
           document.getElementsByClassName('friend-drawer selected_user')[i].className = "friend-drawer friend-drawer--onhover";
        }
        document.getElementById("myForm").style.display = "block";
        document.getElementById("openChatBtn").style.display = "none";
        document.getElementById('messageTextArea').style.display = "none"
    }

    function loadMessageByChatId(receiver_id){
        $http({
            method: 'POST',
            url: "/getChatMessages?receiver_id="+receiver_id+"&chat_id="+$scope.chat_id,
        }).then(function (d) {
            console.log(d.data);
            $scope.Messages = d.data;
        }, function (error) {
            console.log("error in getChatMessages -> ", error);
        });
    }
    $scope.loadMessageByChatId = function(receiver_id, chat_id, index, count){
        $scope.is_chat=1
        $scope.is_contact=0
        $scope.receiver_id=receiver_id
        $scope.chat_id=chat_id
        for(i=0;i<count;i++){
           document.getElementById("user"+i).className = "friend-drawer friend-drawer--onhover";
        }
        document.getElementById("user"+index).className = "friend-drawer selected_user";
        $scope.selectedUser=$scope.ChatUserRelations.filter(user => user.user_id == receiver_id)[0].user
        console.log($scope.selectedUser)
        document.getElementById('messageTextArea').style.display = "block"
        $(".chat-bubble").hide("slow").show("slow");
        loadMessageByChatId(receiver_id)
    }
    $scope.sendMessage=function(){
        if($scope.Messages.length==0){
            $scope.chat_id=0;
        }
        $scope.model={
            chat_id:$scope.chat_id,
            sender_id:$scope.user_id,
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
            if($scope.is_chat==1){
                loadMessageByChatId($scope.receiver_id)
            }
            if($scope.is_contact==1){
                loadMessageByContactId($scope.receiver_id)
            }
        }, function (error) {
            console.log("error in sendMessage -> ", error);
        });
    }

}]);