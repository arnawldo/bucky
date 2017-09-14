$(function () {
    var $listOfBuckets, $listOfTasks, $newTaskForm, $newBucketForm, $showAddBucketList, $showAddTask, $flashMessages;
    $listOfBuckets = $('#list-of-buckets');
    $listOfTasks = $('#list-of-tasks');
    $newBucketForm = $('#newBucketForm');
    $newTaskForm = $('#newTaskForm');
    $showAddBucketList = $('#showAddBucketList');
    $showAddTask = $('#showAddTask');
    $flashMessages = $('#flash-messages');

    // ADDING A NEW BUCKET

    // bucket form starts hidden
    // $newBucketForm.hide();
    // show form if add bucket button is pressed
    $showAddBucketList.on('click', function () {
        $newBucketForm.slideToggle(500);
    });

    // handle add bucket request
    $newBucketForm.on('submit', function (e) {
        e.preventDefault();

        $.getJSON($SCRIPT_ROOT + '/_create_bucketlist', {
            bucketName: $('input#newBucketName').val()
        }, function (data) {

            if (data.statusCode == true) {
                // bucket created successfully, and bucket element to screen

                var newBucketElement = '<li>' + '<a href=' + data.bucketLink + '>' + data.bucketName + '</a>' + '</li>';
                $(newBucketElement).hide().appendTo($listOfBuckets).fadeIn(1000);
                removeDeleteClass(); // reset delete option

            } else if (data.hasOwnProperty('errorMessage')) {
                // bucket not created, show error message
                displayErrorMessage(data.errorMessage);
            }
            // clear input field
            $('input#newBucketName').val('');
        });
        return false;
    });

    // DELETING BUCKET-LISTS

    // change class of bucket-lists to '.delete'
    $('button#deleteBucketLists').on('click', function (e) {
        $('ul#list-of-buckets>li').each(function () {
            $(this).toggleClass("delete");
        });
    });

    // delete bucket-list on click
    $('ul#list-of-buckets').on(
        'click', // event
        '.delete', // selector
        {}, // data
        function (e) {
            e.preventDefault();
            var $bucket = $(e.target);

            // avoid triggering delete when clicking 'li' instead of an 'a' tag
            if (!$bucket.html().includes('<a')) {
                $.getJSON($SCRIPT_ROOT + '/_delete_bucketlist', {
                    bucketName: $bucket.html().trim()
                }, function (data) {

                    if (data.statusCode == true) {
                        // bucket deleted successfully, remove bucket-list element
                        removeElement($bucket.parent());
                    } else if (data.hasOwnProperty('errorMessage')) {
                // bucket not deleted, show error message
                displayErrorMessage(data.errorMessage);
            }
                });
                return false;
            }
        }
    );

    // ADDING A NEW TASK

    // task form starts hidden
    // $newTaskForm.hide();
    // show form if add task button pressed
    $showAddTask.on('click', function () {
        $newTaskForm.slideToggle(500);
    });

    // handle add task request

    $newTaskForm.on('submit', function (e) {
        e.preventDefault();

        $.getJSON($SCRIPT_ROOT + '/_create_task', {
            taskDescription: $('input#newTaskName').val().trim(),
            bucketName: $('h1#bucket-name').text().trim()
        }, function (data) {

            if (data.statusCode == true) {
                // task successfully created, add task element
                var newTaskElement = '<li>' + data.taskDescription + '</li>';
                $(newTaskElement).hide().appendTo($listOfTasks).fadeIn(1000);
                // clear delete option
                removeDeleteClass();
            } else if (data.hasOwnProperty('errorMessage')) {
                // task not created, show error message
                displayErrorMessage(data.errorMessage);
            }
            // clear input field
            $('input#newTaskName').val('');
        });
        return false;
    });

    // DELETING TASKS

    // change class of tasks to '.delete'
    $('button#deleteTasks').on('click', function () {
        $('ul#list-of-tasks>li').each(function () {
            $(this).toggleClass("delete");
        });
    });

    // delete task on click
    $('ul#list-of-tasks').on(
        'click', // event
        '.delete', // selector
        {}, // data
        function (e) {

            $.getJSON($SCRIPT_ROOT + '/_delete_task', {
                taskDescription: e.target.textContent.trim(),
                bucketName: $('h1#bucket-name').text().trim()
            }, function (data) {

                if (data.statusCode == true) {
                    // task successfully deleted, remove task element
                    var $taskElement = $(e.target);
                    removeElement($taskElement);
                } else if (data.hasOwnProperty('errorMessage')) {
                // task not deleted, show error message
                displayErrorMessage(data.errorMessage);
            }
            });
            return false;
        }
    );

    // HELPER FUNCTIONS

    // function to display error messages to user
    function displayErrorMessage(errorMessage) {
        var flashMessage = '<div class="alert alert-warning">' +
            '<button type="button" class="close" data-dismiss="alert">&times;</button>' +
            errorMessage +
            '</div>';
        $(flashMessage).hide().appendTo($flashMessages).fadeIn(1000);
    }

    // function to remove 'delete' class
    function removeDeleteClass() {
        $('ul#list-of-tasks>li').each(function () {
            $(this).removeClass("delete");
        });
        $('ul#list-of-buckets>li').each(function () {
            $(this).removeClass("delete");
        });

    }

    // function to remove element
    function removeElement($elemnt) {
        $elemnt.animate({
            opacity: 0.0,
            height: '-=40'
        }, 500, function () {
            $elemnt.remove();
        });
    }


});
