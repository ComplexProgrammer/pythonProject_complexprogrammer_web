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
        $scope.photo_url=$scope.user.photo_url;
        $scope.name=$scope.user.name;
        $scope.email=$scope.user.email;
        $scope.phone=$scope.user.phone;
        $scope.provider_id=$scope.user.provider_id;
        $scope.uid=$scope.user.uid;
        if($scope.user.name)
            $scope.login=$scope.user.name;
        else
            if($scope.user.email)
                $scope.login=$scope.user.email;
            else
                if($scope.user.phone)
                    $scope.login=$scope.user.phone;
    }
    function getUsers(){
            $http({
                method: 'POST',
                url: "/getUser?uid="+$scope.uid+"&not_me=1",
            }).then(function (d) {
                $scope.ShowData = true;
                console.log(d.data);
                $scope.Users = d.data;
            }, function (error) {
                console.log("error in GetImageCompareResult -> ", error);
            });
    }
    $scope.openForm = function() {
        if($scope.Users==null){
            getUsers()
        }
        document.getElementById("myForm").style.display = "block";
        document.getElementById("openChatBtn").style.display = "none";
        document.getElementById('messageTextArea').style.display = "none"

    }
    $scope.loadMessageByUserId = function(id){
        $scope.selectedUser=$scope.Users.filter(user => user.id == id)[0]
        document.getElementById('messageTextArea').style.display = "block"
        $(".chat-bubble").hide("slow").show("slow");
    }

}]);