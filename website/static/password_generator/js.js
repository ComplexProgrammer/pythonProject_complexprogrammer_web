var app = angular.module("App", []);
    app.controller("PasswordGenerator", ["$scope", "$http", "$filter", function ($scope, $http, $filter) {
    $scope.ShowData = false;
    $scope.Model = {}
    var slider = document.getElementById("myRange");
    $scope.Model.PasswordLength = slider.value;
    document.getElementById('rangeValue').innerHTML = slider.value;
    slider.oninput = function() {
        $scope.Model.PasswordLength = this.value;
        document.getElementById('rangeValue').innerHTML = slider.value;
        LoadData()
    }
    $scope.Model.Uppercase = true;
    $scope.Model.Lowercase = true;
    $scope.Model.Numbers = true;
    $scope.Model.Symbols = true;
    LoadData()
    function LoadData(){
        document.getElementById('conn').style.visibility = "visible";
        $http({
            method: 'POST',
            url: "/password_generator",
            data: JSON.stringify($scope.Model),
            dataType: "json"
            }).then(function (d) {
                console.log(d.data.result);
                $scope.Password=d.data.result;
                alertify.error($scope.Password);
                document.getElementById('conn').style.visibility = "hidden";
            }, function (error) {
            document.getElementById("Password").value="";
                document.getElementById('conn').style.visibility = "hidden";
                alertify.error("Xatolik yuz berdi");
                console.log("error in password_generator -> ", error);
        });
    }
    $scope.Refresh=function() {
        LoadData()
    };
    $scope.Copy=function(){
        document.getElementById("Password").disabled = false;
        var copyText = document.getElementById("Password");
        copyText.select();
        copyText.setSelectionRange(0, 99999);
        document.execCommand("copy");
        alertify.success("Copied");
        document.getElementById("Password").disabled = true;
    }


}]);