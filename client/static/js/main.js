"use strict";

jQuery.noConflict();
jQuery(document).ready(function ($) {
  // Map form data to json
  jQuery("form").on("submit", function (e) {
    let data = $(this).serializeJSON();
    const method = data.method || this.method;
    delete data.method;

    jQuery.ajax({
      type: method,
      url: this.action,
      dataType: "json",
      data: JSON.stringify($(this).serializeJSON()),
      success: function (data) {
        if (data.redirect_to) window.location.replace(data.redirect_to);
      },
      contentType: "application/json",
      error: function (error) {
        let error_mapped = JSON.parse(error.responseText);
        let error_message = "";
        if (Array.isArray(error_mapped.detail))
          error_message = error_mapped.detail[0].msg;
        else error_message = error_mapped.detail;
        alert(error_message);
      },
    });

    e.preventDefault();
  });
});
