var app = angular.module("App", []);
    app.controller("InstagramDownloader", ["$scope", "$http", "$filter", function ($scope, $http, $filter) {
        $scope.Paste=function(){
            navigator.clipboard.readText().then((clipText) => ($scope.instagram_user_name = clipText, document.getElementById('instagram_user_name').value = clipText ));
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
}]);