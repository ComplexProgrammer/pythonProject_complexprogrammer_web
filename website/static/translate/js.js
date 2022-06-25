var app = angular.module("App", []);
    app.controller("Translate", ["$scope", "$http", "$filter", function ($scope, $http, $filter) {

    $scope.ShowData = false;
    $scope.getResult=function(text) {
        document.getElementById('conn').style.visibility = "visible";
        $http({
            method: 'POST',
            url: "/GetTranslateResult?text="+text,
        }).then(function (d) {
            $scope.ShowData = true;
            console.log(d.data.data);
            $scope.Data = d.data.data;
            $scope.result=$scope.Data;
            if($scope.Data==0){
                alertify.error("Rasm o`lchamlari bir xil emas. \n\n\n Iltimos bir xil o`lchamdagi rasm kiriting.");
            }
            else{
                alertify.success("Natija tayyor");
            }
            document.getElementById('conn').style.visibility = "hidden";
        }, function (error) {
            $scope.ShowData = false;
            alertify.error("Xatolik yuz berdi");
            console.log("error in GetTranslateResult -> ", error);
            document.getElementById('conn').style.visibility = "hidden";
        });
    };
}]);