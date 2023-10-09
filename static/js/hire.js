$(document).ready(function() {
    $("#jobSearchForm").submit(function(event) {  // Add the event parameter
        // Prevent the default form submission
        event.preventDefault();

        // Get the form action URL
        var formAction = $(this).attr("action");

        // Serialize the form data
        var formData = $(this).serialize();

        // Redirect to the search results page with the form data
        window.location.href = formAction + "?" + formData;
    });
});
