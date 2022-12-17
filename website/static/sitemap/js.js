var app = angular.module("App", []);
    app.controller("SitemapGenerator", ["$scope", "$http", "$filter", function ($scope, $http, $filter) {
    $scope.ShowData = false;
    function LoadData(){
        document.getElementById('conn').style.visibility = "visible";
        $http({
            method: 'POST',
            url: "/sitemap",
            data: JSON.stringify($scope.url),
            dataType: "json"
            }).then(function (d) {
                console.log(d.data.result);
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
                alertify.success('Success!');
                document.getElementById('conn').style.visibility = "hidden";
            }, function (error) {
                document.getElementById("url").value="";
                document.getElementById('conn').style.visibility = "hidden";
                alertify.error("Error");
                console.log("error in sitemap -> ", error);
        });
    }
    $scope.Generator=function() {
        LoadData()
    };


}]);