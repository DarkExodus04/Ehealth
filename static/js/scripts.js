$("#signup").submit(function (e) {
  var $form = $(this);
  var $error = $form.find(".error");
  var data = $form.serialize();

  $.ajax({
    url: "/user/signup",
    type: "POST",
    data: data,
    dataType: "json",
    success: function (resp) {
      window.location.href = "/pdashboard/";
    },
    error: function (resp) {
      $error.text(resp.responseJSON.error).removeClass("error--hidden");
    },
  });

  e.preventDefault();
});

$("#login").submit(function (e) {
  var $form = $(this);
  var $error = $form.find(".error");
  var data = $form.serialize();

  $.ajax({
    url: "/user/login",
    type: "POST",
    data: data,
    dataType: "json",
    success: function (resp) {
      window.location.href = "/pdashboard/";
    },
    error: function (resp) {
      $error.text(resp.responseJSON.error).removeClass("error--hidden");
    },
  });

  e.preventDefault();
});

$("form[name='doctor-signup']").submit(function (e) {
  var $form = $(this);
  var $error = $form.find(".error");
  var data = $form.serialize();

  $.ajax({
    url: "/doc/signup",
    type: "POST",
    data: data,
    dataType: "json",
    success: function (resp) {
      window.location.href = "/ddashboard/";
    },
    error: function (resp) {
      $error.text(resp.responseJSON.error).removeClass("error--hidden");
    },
  });

  e.preventDefault();
});
