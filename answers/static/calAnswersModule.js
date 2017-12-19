var app = angular.module("calAnswers", []);

app.controller("myCtrl", function($scope, $http) {
    $scope.showRecords = function() {
        $http({
            method: "POST",
            url: "/getRecords",
            data: $scope.searchEntry
        }).then(function(response) {
            $scope.records = response.data;
        }, function(error) {
            console.log(error);
    });
    }

    $scope.searchEntryChanged = function() {
        $scope.showRecords()
    }
});