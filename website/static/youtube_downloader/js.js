var app = angular.module("App", []);
    app.controller("YoutubeDownloader", ["$scope", "$http", "$filter", function ($scope, $http, $filter) {
        $scope.convert_choice = 1;
        $scope.convert_quality = "low";
        $scope.UrlTo = function(choice){
            $scope.convert_choice = choice;
            if(choice==1){
                document.getElementById('quality-tab').style = "display:visible";
            }
            else{
                document.getElementById('quality-tab').style = "display:none";
            }
        }
        $scope.Quality = function(quality){
            $scope.convert_quality = quality
        }
        $scope.Paste=function(){
            navigator.clipboard.readText().then((clipText) => ($scope.link = clipText, document.getElementById('link').value = clipText ));
        }
        $scope.youtube_downloader = function(){
            document.getElementById('conn').style.visibility = "visible";
            document.getElementById('hh').className= "modal-backdrop fade show";
            $scope.links = $scope.link.split(",");
            console.log($scope.link)
            console.log($scope.links)
            $scope.model = {
                choice:$scope.convert_choice,
                quality:$scope.convert_quality,
                link:$scope.link,
                links:$scope.links
            }
            console.dir($scope.model)
            $http({
                method: 'POST',
                url: "/youtube_downloader",
                data: JSON.stringify($scope.model),
                dataType: "json"
            }).then(function (d) {
                if(d.data.result=="0"){
                    alertify.error("Youtube video url manzili kiritilmagan");
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
                console.log("error in youtube_downloader -> ", error);
            });
        }
}]);