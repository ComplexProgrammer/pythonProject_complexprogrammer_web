var app = angular.module("App", []);
    app.directive('ngFiles', ['$parse', function ($parse) {
        function fn_link(scope, element, attrs) {
            var onChange = $parse(attrs.ngFiles);
            element.on('change', function (event) {
                onChange(scope, { $files: event.target.files });
            });
        };
        return {
            link: fn_link
        }
    } ]).controller("ImageCompare", ["$scope", "$http", "$filter", function ($scope, $http, $filter) {
    $scope.imageSrc = "";
    var formdata = new FormData();
    $scope.getTheFiles1 = function ($files) {
        formdata.set('img1', $files[0]);
        console.log($files[0]);
//        angular.forEach($files, function (value, key) {
//            console.log(value);
//            console.log(formdata);
//        });
    };
    $scope.getTheFiles2 = function ($files) {
        formdata.set('img2', $files[0]);
        console.log($files[0]);
    };
    $scope.ShowData = false;
    $scope.getResult=function() {
        console.log(formdata.get('img1'));
        console.log(formdata.get('img2'));
        if(formdata.get('img1')==null||formdata.get('img2')==null){
            alertify.error("Rasmlar tanlanmagan");
        }
        else{
            document.getElementById('conn').style.visibility = "visible";
            $http({
                method: 'POST',
                url: "/GetImageCompareResult",
                data: formdata,
                headers: {
                    'Content-Type': undefined
                }
            }).then(function (d) {
                $scope.ShowData = true;
                console.log(d.data.data);
                $scope.Data = d.data.data;
                $scope.img_result=$scope.Data;
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
                console.log("error in GetImageCompareResult -> ", error);
                document.getElementById('conn').style.visibility = "hidden";
            });
        }


    };
}]);