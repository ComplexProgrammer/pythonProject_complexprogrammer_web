var app = angular.module("App", []);
    app.controller("Translate", ["$scope", "$http", "$filter", function ($scope, $http, $filter) {
    var text = document.getElementById('text');
    text.focus();
    $scope.ShowData = false;
    $scope.src = "english";
    $scope.dest = "uzbek";
    $http({
        method: 'POST',
        url: "/GetTranslateLanguages",
        }).then(function (d) {
            console.log(d.data.data);
            $scope.Languages=d.data.data;
        }, function (error) {
            alertify.error("Xatolik yuz berdi");
            console.log("error in GetTranslateLanguages -> ", error);
    });
    $scope.getResult=function() {
        document.getElementById('conn').style.visibility = "visible";
        $http({
            method: 'POST',
            url: "/GetTranslateResult?text="+$scope.text+"&src="+$scope.src+"&dest="+$scope.dest,
        }).then(function (d) {
            $scope.ShowData = true;
            console.log(d.data.data);
            $scope.Data = d.data.data;
            $scope.result=$scope.Data;
            $http({
                method: 'POST',
                url: "/TextToSpeech?text="+$scope.result,
                }).then(function (d) {
                    console.log(d.data.data);
                }, function (error) {
                    console.log("error in TextToSpeech -> ", error);
            });
            alertify.success("Natija tayyor");
            document.getElementById('conn').style.visibility = "hidden";
        }, function (error) {
            $scope.ShowData = false;
            alertify.error("Xatolik yuz berdi");
            console.log("error in GetTranslateResult -> ", error);
            document.getElementById('conn').style.visibility = "hidden";
        });
    };
}]);