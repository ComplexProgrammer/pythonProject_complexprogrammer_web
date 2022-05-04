var app = angular.module("App", []);
app.controller("ImageCompare", ["$scope", "$http", "$filter", function ($scope, $http, $filter) {
    $scope.ShowData = false;
    $scope.getResult=function() {
        var f = document.getElementById('img1').files[0],
        r = new FileReader();

        r.onloadend = function(e) {
          var data = e.target.result;
          console.log(e);
          console.log(e.target);
          console.log(data);
          //send your binary data via $http or $resource or do anything else with it
        }

        r.readAsBinaryString(f);
        document.getElementById('conn').style.visibility = "visible";
        $http({
            method: 'GET',
            url: "/GetImageCompareResult",
            dataType: "json"
        }).then(function (d) {
            $scope.Data = d.data.data;
            if (d.data === 0) {
                $scope.ShowData = false;
            }
            else {
                if (d.data === -1) {
                    $scope.ShowData = false;
                }
                else {
                    if (d.data.length === 0) {
                        $scope.ShowData = false;
                    }
                    else {
                        $scope.ShowData = true;
                    }
                }
            }
            document.getElementById('conn').style.visibility = "hidden";
        }, function (error) {
            console.log("error in GetImageCompareResult -> ", error);
            document.getElementById('conn').style.visibility = "hidden";
        });
    };
}]);