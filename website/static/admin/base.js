var app = angular.module("App", []);
app.filter('jsonDate', ['$filter', function ($filter) {
    return function (input, format) {
        return (input)
            ? $filter('date')(parseInt(input.substr(6)), format)
            : '';
    };
}]);
app.controller("Base", ["$scope", "$window", "$http", "$filter", function ($scope, $window, $http, $filter) {
    $scope.show_groups_data = false;
    get_groups()
    function get_groups(){
        document.getElementById('hh').className= "modal-backdrop fade show";
        document.getElementById('conn').style.visibility = "visible";
        $http({
            method: 'GET',
            url: "/get_groups"
        }).then(function (d) {
            if (d.data.length > 0) {
                $scope.show_groups_data = true;
            }
            else {
                $scope.show_groups_data = false;
            }
            $scope.groups = d.data;
            console.log($scope.groups);
        }, function (error) {
            console.log("error in get_groups -> ", error);
        });
        document.getElementById('hh').className= "fade hide";
        document.getElementById('conn').style.visibility = "hidden";
    }
    $scope.add_edit_group = function(model){
        if(model===0){
//            $scope.group = {
//                id: 0,
//                number:0,
//                name_en_us:'',
//                name_ru_ru:'',
//                name_uz_crl:'',
//                name_uz_uz:''
//            };
        }
        else{
            $scope.group=model;
        }
    }
    $scope.save_group = function(){
        document.getElementById('hh').className= "modal-backdrop fade show";
        document.getElementById('conn').style.visibility = "visible";
        $http({
            method: 'POST',
            url: "/save_group",
            data: JSON.stringify($scope.Group),
            dataType: "json"
        }).then(function (d) {
            console.log(d);
            console.log(d.data);
            if (d.data === 0) {
                alertify.error("Ma`lumotni saqlashda xatolik yuz berdi");
            }
            else {
                alertify.success("Ma`lumot saqlandi!!!");
                get_groups();
            }
        }, function (error) {
            console.log("error in SAVE_MARKS_APPLICANT -> ", error);
            alertify.error("Ma`lumotni saqlashda xatolik yuz berdi");
        });
        $("#group_modal").modal('hide');
        document.getElementById('hh').className= "fade hide";
        document.getElementById('conn').style.visibility = "hidden";
    }
    $scope.remove_group=function(model){
        document.getElementById('hh').className= "modal-backdrop fade show";
        document.getElementById('conn').style.visibility = "visible";
        alertify.confirm('Remove Group', 'Confirm Remove Group '+model.name_uz_uz, function(){
                $http({
                    method: 'POST',
                    url: "/remove_group?id=" + model.id
                }).then(function (d) {
                    if (d.data === 0) {
                        alertify.error("Ma`lumotni o`chirishda xatolik yuz berdi");
                        document.getElementById('hh').className= "fade hide";
                        document.getElementById('conn').style.visibility = "hidden";
                    }
                    else {
                        alertify.success("Ma`lumot o`chirildi!!!");
                        get_groups();
                    }
                }, function (error) {
                    console.log("error in remove_group -> ", error);
                    alertify.error("Ma`lumotni o`chirishda xatolik yuz berdi");
                    document.getElementById('hh').className= "fade hide";
                    document.getElementById('conn').style.visibility = "hidden";
                });
            }, function(){
                    alertify.error('Cancel')
                    document.getElementById('hh').className= "fade hide";
                    document.getElementById('conn').style.visibility = "hidden";
                }).set('defaultFocus', 'cancel');
    }
}]);