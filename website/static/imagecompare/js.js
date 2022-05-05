var app = angular.module("App", []);
app.controller("ImageCompare", ["$scope", "$http", "$filter","fileReader", function ($scope, $http, $filter, fileReader) {
    $scope.imageSrc = "";

    $scope.$on("fileProgress", function (e, progress) {
        $scope.progress = progress.loaded / progress.total;
    });
    $scope.ShowData = false;
    $scope.getResult=function() {
        document.getElementById('conn').style.visibility = "visible";
        $http({
            method: 'GET',
            url: "/GetImageCompareResult?img_model1="+$scope.img_model1+"&img_model2="+$scope.img_model2,
            dataType: "json"
        }).then(function (d) {
            console.log(d.data.data);
            $scope.Data = d.data.data;
            $scope.img_result=$scope.Data;
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

app.directive("ngFileSelect", function (fileReader, $timeout) {
  return {
    scope: {
      ngModel: "="
    },
    link: function ($scope, el) {
      function getFile(file) {
        fileReader.readAsDataUrl(file, $scope).then(function (result) {
          $timeout(function () {
            $scope.ngModel = result;
          });
        });
      }

      el.bind("change", function (e) {
        var file = (e.srcElement || e.target).files[0];
        getFile(file);
      });
    }
  };
});

app.factory("fileReader", function ($q, $log) {
  var onLoad = function (reader, deferred, scope) {
    return function () {
      scope.$apply(function () {
        deferred.resolve(reader.result);
      });
    };
  };

  var onError = function (reader, deferred, scope) {
    return function () {
      scope.$apply(function () {
        deferred.reject(reader.result);
      });
    };
  };

  var onProgress = function (reader, scope) {
    return function (event) {
      scope.$broadcast("fileProgress", {
        total: event.total,
        loaded: event.loaded
      });
    };
  };

  var getReader = function (deferred, scope) {
    var reader = new FileReader();
    reader.onload = onLoad(reader, deferred, scope);
    reader.onerror = onError(reader, deferred, scope);
    reader.onprogress = onProgress(reader, scope);
    return reader;
  };

  var readAsDataURL = function (file, scope) {
    var deferred = $q.defer();

    var reader = getReader(deferred, scope);
    reader.readAsDataURL(file);

    return deferred.promise;
  };

  return {
    readAsDataUrl: readAsDataURL
  };
});