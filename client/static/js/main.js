"use strict";

jQuery.noConflict();
jQuery(document).ready(function ($) {
  // Map form data to json
  jQuery("form").on("submit", function (e) {
    jQuery.ajax({
      type: "POST",
      url: this.action,
      dataType: "json",
      data: JSON.stringify($(this).serializeJSON()),
      success: function (data) {
        console.log(data);
        if (data.redirect_to) window.location.replace(data.redirect_to);
      },
      contentType: "application/json",
    });

    e.preventDefault();
  });
});
