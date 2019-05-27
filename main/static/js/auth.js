

jQuery(function ($) {
    django.jQuery(".get_token_form").hide();
    $('.phone_number_form').on('click', '.send_sms',function (e) {
        let $self = $(this);
        let phone_number = $self.parent().find('.phone_number').val();
        let url = 'send/sms/';
        let bot_id = $self.parent().find('.bot_id').val();

        var data = {'phone_number': phone_number.toString(), 'bot_id': bot_id};

        $.ajax({
            url: url,
            type: "POST",
            contentType: 'application/json',
            data: JSON.stringify(data),

            success: function (json) {
            if (json.status === 'ok') {
                django.jQuery(".get_token_form").show();
                django.jQuery(".phone_number_form").hide();
            }
            },

            error: function (xhr, errmsg, err) {
                console.log(json);
            }
        });
    });

    $('.get_token_form').on('click', '.get_token',function (e) {
        let $self = $(this);
        let phone_number = $self.parent().find('.phone_number').val();
        let sms_code = $self.parent().find('.sms_code').val();
        let bot_id = $self.parent().find('.bot_id').val();
        let url = 'get/token/';

        var data = {'phone_number': phone_number.toString(), 'otp_code': sms_code.toString(), 'bot_id': bot_id};

        $.ajax({
            url: url,
            type: "POST",
            contentType: 'application/json',
            data: JSON.stringify(data),

            success: function (json) {
            if (json.status === 'ok') {
                django.jQuery(".get_token_form").hide();
                location.reload();
            }
            },

            error: function (xhr, errmsg, err) {
                console.log(json);
            }
        });
    });
        $('.get_token_auto').on('click', '.get_token_auto',function (e) {
        let $self = $(this);
        let bot_id = $self.parent().find('.bot_id').val();
        let url = 'get/token/';

        var data = {'bot_id': bot_id};

        $.ajax({
            url: url,
            type: "POST",
            contentType: 'application/json',
            data: JSON.stringify(data),

            success: function (json) {
            if (json.status === 'ok') {
                django.jQuery(".get_token_form").hide();
                location.reload();
            }
            },

            error: function (xhr, errmsg, err) {
                console.log(json);
            }
        });
    });

});

