jQuery.validator.addMethod("hasDigit", function (value, element) {
    return this.optional(element) || hasDigit(value);
});

jQuery.validator.addMethod("hasLowerCase", function (value, element) {
    return this.optional(element) || hasLowerCase(value);
});

jQuery.validator.addMethod("hasUpperCase", function (value, element) {
    return this.optional(element) || hasUpperCase(value);
});

jQuery.validator.addMethod("alphanumeric", function (value, element) {
    return this.optional(element) || alphanumeric(value);
});

$("#signup").click(function () {
    $("#first").fadeOut("fast", function () {
        $("#second").fadeIn("fast");
    });
});

$("#signin").click(function () {
    $("#second").fadeOut("fast", function () {
        $("#first").fadeIn("fast");
    });
});

$(function () {
    $("form[name='login']").validate({
        rules: {
            email: {
                required: true,
                email: true,
            },
            password: {
                required: true,
            }
        },
        messages: {
            email: "Please enter a valid email address",

            password: {
                required: "Please enter password",
            }

        },
        submitHandler: function (form) {
            form.submit();
        }
    });
});


$(function () {

    $("form[name='registration']").validate({
        rules: {
            username: {
                required: true,
                alphanumeric: true,
            },
            email: {
                required: true,
                email: true,
            },
            password1: {
                required: true,
                minlength: 8,
                hasDigit: true,
                hasLowerCase: true,
                hasUpperCase: true,
            },
            password2: {
                equalTo: "#password1"
            },
        },
        messages: {
            username: {
                required: "Please enter a username",
                alphanumeric: "Only latin letters and numbers are allowed in username"
            },
            email: "Please enter a valid email address",
            password1: {
                required: "Please provide a password",
                minlength: "Password must be at least 8 characters long",
                hasDigit: "Password must contain at least one digit",
                hasUpperCase: "Password must contain at least one uppercase latin letter",
                hasLowerCase: "Password must contain at least one lowercase latin letter",
            },
            password2: {
                equalTo: "Passwords do not match",
            },
        },

        submitHandler: function (form) {
            form.submit();
        }

    });
});

function alphanumeric(str) {
    let letterNumber = /^[0-9a-zA-Z]+$/;
    return (str.value.match(letterNumber));
}

function hasDigit(str) {
    return /\d/.test(str);
}

function hasLowerCase(str) {
    return /[a-z]/.test(str);
}

function hasUpperCase(str) {
    return /[A-Z]/.test(str);
}