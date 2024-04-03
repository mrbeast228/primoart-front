function toggleVisibility(buttonId, elementToToggleId) {
    // Toggle visibility of the element
    $("#" + elementToToggleId).toggle();

    // Get value from hidden input and append to the content if the element is visible
    //if ($("#" + elementToToggleId).is(":visible")) {
    //    var valueFromHiddenInput = $("#" + hiddenInputId).val();
    //    $("#" + elementToToggleId).append(valueFromHiddenInput);
    //}

    // Toggle class of the button
    $("#" + buttonId).toggleClass("active");
}