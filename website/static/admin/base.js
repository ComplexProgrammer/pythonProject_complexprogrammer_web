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
            document.getElementById('hh').className= "fade hide";
            document.getElementById('conn').style.visibility = "hidden";
        }, function (error) {
            console.log("error in get_groups -> ", error);
            document.getElementById('hh').className= "fade hide";
        document.getElementById('conn').style.visibility = "hidden";
        });
    }
    $window.get_groups =function (){
        get_groups()
    }
    $scope.add_edit_group = function(model){
        group_modal.show();
        if(model===0){
            $scope.modal_title='Add'
           $scope.group = {
               id: 0
           };
        }
        else{
            $scope.modal_title='Edit'
            $scope.group=model;
        }
    }
    $scope.save_group = function(){
        document.getElementById('hh').className = "modal-backdrop fade show";
        document.getElementById('conn').style.visibility = "visible";
        $http({
            method: 'POST',
            url: "/save_group",
            data: JSON.stringify($scope.group),
            dataType: "json"
        }).then(function (d) {
            console.log(d);
            console.log(d.data);
            if (d.data.data === 0) {
                alertify.error("Ma`lumotni saqlashda xatolik yuz berdi");
                document.getElementById('hh').className= "fade hide";
                document.getElementById('conn').style.visibility = "hidden";
            }
            else {
                alertify.success("Ma`lumot saqlandi!!!");
                group_modal.hide();
                get_groups();
            }
        }, function (error) {
            console.log("error in save_group -> ", error);
            alertify.error("Ma`lumotni saqlashda xatolik yuz berdi");
            document.getElementById('hh').className= "fade hide";
            document.getElementById('conn').style.visibility = "hidden";
        });
    }
    $scope.remove_group=function(model){
        document.getElementById('hh').className= "modal-backdrop fade show";
        document.getElementById('conn').style.visibility = "visible";
        alertify.confirm('Remove Group', 'Confirm Remove Group '+model.name_uz_uz, function(){
                $http({
                    method: 'POST',
                    url: "/remove_group?id=" + model.id
                }).then(function (d) {
                    if (d.data.data === 0) {
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

    $scope.show_books_data = false;
    var group_id;
    function get_books(){
       // group_id= document.getElementById('group_id').value;
        document.getElementById('hh').className= "modal-backdrop fade show";
        document.getElementById('conn').style.visibility = "visible";
        $http({
            method: 'GET',
            url: "/get_books?group_id="+group_id
        }).then(function (d) {
            if (d.data.length > 0) {
                $scope.show_books_data = true;
            }
            else {
                $scope.show_books_data = false;
            }
            $scope.books = d.data;
            document.getElementById('hh').className= "fade hide";
            document.getElementById('conn').style.visibility = "hidden";
        }, function (error) {
            console.log("error in get_books -> ", error);
            document.getElementById('hh').className= "fade hide";
        document.getElementById('conn').style.visibility = "hidden";
        });
    }
    $window.get_books = function (id){
        group_id=id
        get_books()
    }
    $scope.add_edit_book = function(model){
        book_modal.show();
        if(model===0){
            $scope.modal_title='Add'
            $scope.book = {
                id: 0,
                group_id:group_id
            };
        }
        else{
            $scope.modal_title='Edit'
            $scope.book=model;
        }
    }
    $scope.save_book = function(){
        document.getElementById('hh').className = "modal-backdrop fade show";
        document.getElementById('conn').style.visibility = "visible";
        $http({
            method: 'POST',
            url: "/save_book",
            data: JSON.stringify($scope.book),
            dataType: "json"
        }).then(function (d) {
            console.log(d);
            console.log(d.data);
            if (d.data.data === 0) {
                alertify.error("Ma`lumotni saqlashda xatolik yuz berdi");
                document.getElementById('hh').className= "fade hide";
                document.getElementById('conn').style.visibility = "hidden";
            }
            else {
                alertify.success("Ma`lumot saqlandi!!!");
                book_modal.hide();
                get_books();
            }
        }, function (error) {
            console.log("error in save_book -> ", error);
            alertify.error("Ma`lumotni saqlashda xatolik yuz berdi");
            document.getElementById('hh').className= "fade hide";
            document.getElementById('conn').style.visibility = "hidden";
        });
    }
    $scope.remove_book=function(model){
        document.getElementById('hh').className= "modal-backdrop fade show";
        document.getElementById('conn').style.visibility = "visible";
        alertify.confirm('Remove Book', 'Confirm Remove Book '+model.name_uz_uz, function(){
                $http({
                    method: 'POST',
                    url: "/remove_book?id=" + model.id
                }).then(function (d) {
                    if (d.data.data === 0) {
                        alertify.error("Ma`lumotni o`chirishda xatolik yuz berdi");
                        document.getElementById('hh').className= "fade hide";
                        document.getElementById('conn').style.visibility = "hidden";
                    }
                    else {
                        alertify.success("Ma`lumot o`chirildi!!!");
                        get_books();
                    }
                }, function (error) {
                    console.log("error in remove_book -> ", error);
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

    $scope.show_topics_data = false;
    var book_id;
    function get_topics(){
        document.getElementById('hh').className= "modal-backdrop fade show";
        document.getElementById('conn').style.visibility = "visible";
        $http({
            method: 'GET',
            url: "/get_topics?book_id="+book_id
        }).then(function (d) {
            if (d.data.length > 0) {
                $scope.show_topics_data = true;
            }
            else {
                $scope.show_topics_data = false;
            }
            $scope.topics = d.data;
            document.getElementById('hh').className= "fade hide";
            document.getElementById('conn').style.visibility = "hidden";
        }, function (error) {
            console.log("error in get_topics -> ", error);
            document.getElementById('hh').className= "fade hide";
        document.getElementById('conn').style.visibility = "hidden";
        });
    }
    $window.get_topics = function (id){
        book_id=id;
        get_topics()
    }
    $scope.add_edit_topic = function(model){
        console.log(model)
        topic_modal.show();
        if(model===0){
            $scope.modal_title='Add'
            $scope.topic = {
                id: 0,
                book_id:book_id
            };
        }
        else{
            $scope.modal_title='Edit'
            $scope.topic=model;
        }
    }
    $scope.save_topic = function(){
        document.getElementById('hh').className = "modal-backdrop fade show";
        document.getElementById('conn').style.visibility = "visible";
        $http({
            method: 'POST',
            url: "/save_topic",
            data: JSON.stringify($scope.topic),
            dataType: "json"
        }).then(function (d) {
            console.log(d);
            console.log(d.data);
            if (d.data.data === 0) {
                alertify.error("Ma`lumotni saqlashda xatolik yuz berdi");
                document.getElementById('hh').className= "fade hide";
                document.getElementById('conn').style.visibility = "hidden";
            }
            else {
                alertify.success("Ma`lumot saqlandi!!!");
                topic_modal.hide();
                get_topics();
            }
        }, function (error) {
            console.log("error in save_topic -> ", error);
            alertify.error("Ma`lumotni saqlashda xatolik yuz berdi");
            document.getElementById('hh').className= "fade hide";
            document.getElementById('conn').style.visibility = "hidden";
        });
    }
    $scope.remove_topic=function(model){
        document.getElementById('hh').className= "modal-backdrop fade show";
        document.getElementById('conn').style.visibility = "visible";
        alertify.confirm('Remove Topic', 'Confirm Remove Topic '+model.name_uz_uz, function(){
                $http({
                    method: 'POST',
                    url: "/remove_topic?id=" + model.id
                }).then(function (d) {
                    if (d.data.data === 0) {
                        alertify.error("Ma`lumotni o`chirishda xatolik yuz berdi");
                        document.getElementById('hh').className= "fade hide";
                        document.getElementById('conn').style.visibility = "hidden";
                    }
                    else {
                        alertify.success("Ma`lumot o`chirildi!!!");
                        get_topics();
                    }
                }, function (error) {
                    console.log("error in remove_topic -> ", error);
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

    $scope.show_questions_data = false;
    var topic_id;
    function get_questions(){
        document.getElementById('hh').className= "modal-backdrop fade show";
        document.getElementById('conn').style.visibility = "visible";
        $http({
            method: 'GET',
            url: "/get_questions?topic_id="+topic_id
        }).then(function (d) {
            if (d.data.length > 0) {
                $scope.show_questions_data = true;
            }
            else {
                $scope.show_questions_data = false;
            }
            $scope.questions = d.data;
            document.getElementById('hh').className= "fade hide";
            document.getElementById('conn').style.visibility = "hidden";
        }, function (error) {
            console.log("error in get_questions -> ", error);
            document.getElementById('hh').className= "fade hide";
            document.getElementById('conn').style.visibility = "hidden";
        });
    }
    $window.get_questions = function (id){
        topic_id=id;
        get_questions()
    }
    $scope.add_edit_question = function(model){
        question_modal.show();
        if(model===0){
            $scope.modal_title='Add'
            $scope.question = {
                id: 0,
                topic_id:topic_id
            };
        }
        else{
            $scope.modal_title='Edit'
            $scope.question=model;
        }
    }
    $scope.save_question = function(){
        document.getElementById('hh').className = "modal-backdrop fade show";
        document.getElementById('conn').style.visibility = "visible";
        $http({
            method: 'POST',
            url: "/save_question",
            data: JSON.stringify($scope.question),
            dataType: "json"
        }).then(function (d) {
            console.log(d);
            console.log(d.data);
            if (d.data.data === 0) {
                alertify.error("Ma`lumotni saqlashda xatolik yuz berdi");
                document.getElementById('hh').className= "fade hide";
                document.getElementById('conn').style.visibility = "hidden";
            }
            else {
                alertify.success("Ma`lumot saqlandi!!!");
                question_modal.hide();
                get_questions();
            }
        }, function (error) {
            console.log("error in save_question -> ", error);
            alertify.error("Ma`lumotni saqlashda xatolik yuz berdi");
            document.getElementById('hh').className= "fade hide";
            document.getElementById('conn').style.visibility = "hidden";
        });
    }
    $scope.remove_question=function(model){
        document.getElementById('hh').className= "modal-backdrop fade show";
        document.getElementById('conn').style.visibility = "visible";
        alertify.confirm('Remove Question', 'Confirm Remove Question '+model.name_uz_uz, function(){
                $http({
                    method: 'POST',
                    url: "/remove_question?id=" + model.id
                }).then(function (d) {
                    if (d.data.data === 0) {
                        alertify.error("Ma`lumotni o`chirishda xatolik yuz berdi");
                        document.getElementById('hh').className= "fade hide";
                        document.getElementById('conn').style.visibility = "hidden";
                    }
                    else {
                        alertify.success("Ma`lumot o`chirildi!!!");
                        get_questions();
                    }
                }, function (error) {
                    console.log("error in remove_question -> ", error);
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

    $scope.show_answers_data = false;
    var question_id;
    function get_answers(){
        document.getElementById('hh').className= "modal-backdrop fade show";
        document.getElementById('conn').style.visibility = "visible";
        $http({
            method: 'GET',
            url: "/get_answers?question_id="+question_id
        }).then(function (d) {
            if (d.data.length > 0) {
                $scope.show_answers_data = true;
            }
            else {
                $scope.show_answers_data = false;
            }
            $scope.answers = d.data;
            document.getElementById('hh').className= "fade hide";
            document.getElementById('conn').style.visibility = "hidden";
        }, function (error) {
            console.log("error in get_answers -> ", error);
            document.getElementById('hh').className= "fade hide";
            document.getElementById('conn').style.visibility = "hidden";
        });
    }
    $window.get_answers = function (id){
        question_id=id;
        get_answers()
    }
    $scope.add_edit_answer = function(model){
        answer_modal.show();
        if(model===0){
            $scope.modal_title='Add'
            $scope.answer = {
                id: 0,
                question_id:question_id
            };
        }
        else{
            $scope.modal_title='Edit'
            $scope.answer=model;
        }
    }
    $scope.save_answer = function(){
        document.getElementById('hh').className = "modal-backdrop fade show";
        document.getElementById('conn').style.visibility = "visible";
        $http({
            method: 'POST',
            url: "/save_answer",
            data: JSON.stringify($scope.answer),
            dataType: "json"
        }).then(function (d) {
            console.log(d);
            console.log(d.data);
            if (d.data.data === 0) {
                alertify.error("Ma`lumotni saqlashda xatolik yuz berdi");
                document.getElementById('hh').className= "fade hide";
                document.getElementById('conn').style.visibility = "hidden";
            }
            else {
                alertify.success("Ma`lumot saqlandi!!!");
                answer_modal.hide();
                get_answers();
            }
        }, function (error) {
            console.log("error in save_answer -> ", error);
            alertify.error("Ma`lumotni saqlashda xatolik yuz berdi");
            document.getElementById('hh').className= "fade hide";
            document.getElementById('conn').style.visibility = "hidden";
        });
    }
    $scope.remove_answer=function(model){
        document.getElementById('hh').className= "modal-backdrop fade show";
        document.getElementById('conn').style.visibility = "visible";
        alertify.confirm('Remove Answer', 'Confirm Remove Answer '+model.name_uz_uz, function(){
                $http({
                    method: 'POST',
                    url: "/remove_answer?id=" + model.id
                }).then(function (d) {
                    if (d.data.data === 0) {
                        alertify.error("Ma`lumotni o`chirishda xatolik yuz berdi");
                        document.getElementById('hh').className= "fade hide";
                        document.getElementById('conn').style.visibility = "hidden";
                    }
                    else {
                        alertify.success("Ma`lumot o`chirildi!!!");
                        get_answers();
                    }
                }, function (error) {
                    console.log("error in remove_answer -> ", error);
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