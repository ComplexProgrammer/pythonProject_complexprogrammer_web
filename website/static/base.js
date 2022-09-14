var app = angular.module("App", []);
app.filter('jsonDate', ['$filter', function ($filter) {
    return function (input, format) {
        return (input)
            ? $filter('date')(parseInt(input.substr(6)), format)
            : '';
    };
}]);
app.controller("Base", ["$scope", "$http", "$filter", function ($scope, $http, $filter) {
     function goalert(){
        alert()
    }

    $scope.login="Login";
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
    $scope.openForm = function() {

        if($scope.MyContacts==null){
            getMyContacts()
        }
        for(i=0;i<document.getElementsByClassName('friend-drawer selected_user').length;i++){
           document.getElementsByClassName('friend-drawer selected_user')[i].className = "friend-drawer friend-drawer--onhover";
        }
        document.getElementById("myForm").style.display = "block";
        document.getElementById("openChatBtn").style.display = "none";
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
            if($scope.is_chat==1){
                loadMessageByChatId(d.data[0].chat_id)
            }
            if($scope.is_contact==1){
                loadMessageByContactId($scope.receiver_id)
            }
        }, function (error) {
            console.log("error in sendMessage -> ", error);
        });
    }

}]);