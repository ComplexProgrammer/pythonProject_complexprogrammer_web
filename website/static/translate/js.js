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
    $scope.speech=function(text){
        $http({
            method: 'POST',
            url: "/TextToSpeech?text="+text,
            }).then(function (d) {
                console.log(d.data.data);
            }, function (error) {
                console.log("error in TextToSpeech -> ", error);
        });
    }
    $scope.replace=function(){
        $scope.src1=$scope.src;
        $scope.src=$scope.dest;
        $scope.dest=$scope.src1;
        $scope.text1=$scope.text;
        $scope.text=$scope.result;
        $scope.result=$scope.text1;
    }
    $scope.getResult=function() {
        $scope.result='';
        document.getElementById('hh').className= "modal-backdrop fade show";
        document.getElementById('conn').style.visibility = "visible";
        $http({
            method: 'POST',
            url: "/GetTranslateResult?text="+$scope.text+"&src="+$scope.src+"&dest="+$scope.dest,
        }).then(function (d) {
            $scope.ShowData = true;
            console.log(d.data.data);
            $scope.Data = d.data.data;
            $scope.result=$scope.Data;
            alertify.success("Natija tayyor");
            document.getElementById('hh').className= "fade hide";
            document.getElementById('conn').style.visibility = "hidden";
        }, function (error) {
            $scope.ShowData = false;
            alertify.error("Xatolik yuz berdi");
            console.log("error in GetTranslateResult -> ", error);
            document.getElementById('hh').className= "fade hide";
            document.getElementById('conn').style.visibility = "hidden";
        });
    };
}]);