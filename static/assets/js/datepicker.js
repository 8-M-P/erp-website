$(function () {
  "use strict";
  $(".datepicker").datepicker({
    format: "mm/dd/yyyy",
    todayHighlight: true,
    autoclose: true,
    todayBtn: "linked",
    clearBtn: true,
    language: "tr",
    toggleActive: true,
  });
});
