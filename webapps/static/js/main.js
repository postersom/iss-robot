$(function () {
    // console.log(tests);
    $("#submitScanin").click(function () {

    });
    $(".playbox_send").click(function () {

        var retest = true;

        var deferreds = [];
        var check_sn = $(this).parents(".panel").find(".serial_number").text();
        var uut_log_dir = $(this).parents(".panel").find(".uut_log_dir").val();
        var operation_id = $(this).parents(".panel").find(".operation_id").val();
        var batch_id = $(this).parents(".panel").find(".batch_id").val();
        var test_mode = $(this).parents(".panel").find(".test_mode").val();
        var logop = $(this).parents(".panel").find(".logop").val();
        var product_name = $(this).parents(".panel").find(".product_name").val();
        var result = $(this).parents(".panel").find(".result").val();
        var test_fail = $(this).parents(".panel").find(".test_fail").val();
        var test_abort = $(this).parents(".panel").find(".test_abort").val();
        var message = $(this).parents(".panel").find(".message").val();
        var slot_no = $(this).parents(".panel").find(".slot_no").val();
        var slot_location = $(this).parents(".panel").find(".slot_location").val();
        var code_from = $(this).parents(".panel").find(".code_from").val();
        var datetime = uut_log_dir.split("_");
        datetime = datetime[datetime.length - 1].replace("-", "");
        var robot_path = $(this).parents(".panel").find(".code_version").val();
        var log_template = $(this).parents(".panel").find(".log_template").val();
        log_template = log_template.replace(/==station==/g, test_station);
        log_template = log_template.replace(/==sn==/g, check_sn);
        log_template = log_template.replace(/==chassis==/g, chassis_name);
        log_template = log_template.replace(/==datetime==/g, datetime);
        if (result == "passes") {
            log_template = log_template.replace(/==result==/g, "passed");
        } else {
            log_template = log_template.replace(/==result==/g, result);
        }
        log_template = log_template.replace(/==test_mode==/g, test_mode);
        log_template = log_template.replace(/==product_name==/g, product_name);
        log_template = log_template.replace(/==logop==/g, logop);

        if (check_sn != "-" && check_sn != "") {
            deferreds.push(deliveryout(check_sn, slot_location, test_mode, retest, code_from, logop, uut_log_dir, slot_no, log_template, chassis_name, operation_id, batch_id, result, test_fail, test_abort, message, robot_path));
            console.log("sn:" + check_sn);
        }
    });
    //  get operator id from cookie
    var operation_id = getCookie("operation_id");
    $("#operation_id").val(operation_id);
    //on close batch modal popup
    $('#batchModal').on('hidden.bs.modal', function () {

        var total = $('.batch-col-row').children().length;
        for (var i = 1; i <= total; i++) {
            resetVerify(i);
        }
        var textarea_value2 = $("#operation_id").val();
        if (textarea_value2 != '') {
            $("#submitScanin").removeAttr("disabled");
        } else {
            $("#submitScanin").attr("disabled", "disabled");
        }
    });

    $('#checkoutbatch').on('hidden.bs.modal', function () {

        $.each($(this).find('input[type="checkbox"]'), function (key, value) {
            $(this).prop('checked', false);
        });
    });

    $('#checkoutbatch').on('shown.bs.modal', function () {


        //disable select all checkout popup
        if ($('.checkout-slot input[type="checkbox"]').length == 0) {
            $("#all").attr('disabled', 'disabled');
        }

        //disable select all abort popup
        if ($('.abort-slot input[type="checkbox"]').length == 0) {
            $("#all-abort").attr('disabled', 'disabled');
        }

    });


    // input change event
    $('.batch-sn').on('input propertychange paste', function () {

        $(this).parents(".batch-row-detail").removeClass("verified verified-warning verified-failed");
        $(this).parents(".batch-row-detail").find(".status-text").text("");
        triggerSubmitbutton();
    });
    // click button slot event
    $(".popup").click(function () {
        $("#slot_no").val($(this).attr('id').replace("popup-", ""));
        $(".slot-no-heading").text($(this).attr('id').replace("popup-", ""));

    });

    // checkbox in checkout popup slot event
    $('#checkoutbatch .checkout-slot :checkbox').change(function () {

        var select_all = true;
        $.each($('#checkoutbatch .checkout-slot :checkbox'), function (key, value) {

            if (!value.checked) {
                select_all = false;
                return false;
            }
        });
        $('#all').prop('checked', select_all);
        triggerSubmitdeliveryoutbtn();
    });
    // abort in checkout popup slot event
    $('#abortbatch .abort-slot :checkbox').change(function () {
        var select_all = true;
        $.each($('#abortbatch .abort-slot :checkbox'), function (key, value) {
            if (!value.checked) {
                select_all = false;
                return false;
            }
        });
        $('#all-abort').prop('checked', select_all);
        triggerSubmitabortbtn();
    });
    // select all checkbox in checkout popup event
    $('#all').change(function (e) {
        if (e.currentTarget.checked) {
            $('.checkout-slot').find('input[type="checkbox"]:enabled').prop('checked', true);
        } else {
            $('.checkout-slot').find('input[type="checkbox"]:enabled').prop('checked', false);
        }
        triggerSubmitdeliveryoutbtn();
    });

    // select all checkbox in abort popup event
    $('#all-abort').change(function (e) {
        if (e.currentTarget.checked) {
            $('.abort-slot').find('input[type="checkbox"]:enabled').prop('checked', true);
        } else {
            $('.abort-slot').find('input[type="checkbox"]:enabled').prop('checked', false);
        }
        triggerSubmitabortbtn();
    });

    $("#test-counter").text($('#uutList>.col-sm-3.testing').size());
    $("#failing-counter").text($('#uutList>.col-sm-3.failing').size());
    $("#failed-counter").text($('#uutList>.col-sm-3.failed').size());
    $("#abort-counter").text($('#uutList>.col-sm-3.abort').size());
    $("#pass-counter").text($('#uutList>.col-sm-3.passes').size());

    $('#batchModal').on('hidden.bs.modal', function () {
        $(this)
        $("#operation_id").val('');
    })

    $('#abortbatch').on('shown.bs.modal', function () {

        $("#submitScanin").attr("disabled", "disabled");

        var ck_slot1 = $("#slot-1").attr('class');
        console.log("ck_slot1" + ck_slot1);
        var ck_slot2 = $("#slot-2").attr('class');
        console.log("ck_slot2" + ck_slot2);
        var ck_slot3 = $("#slot-3").attr('class');
        console.log("ck_slot3" + ck_slot3);
        var ck_slot4 = $("#slot-4").attr('class');
        console.log("ck_slot4" + ck_slot4);
        var ck_slot5 = $("#slot-5").attr('class');
        console.log("ck_slot5" + ck_slot5);
        var ck_slot6 = $("#slot-6").attr('class');
        console.log("ck_slot6" + ck_slot6);
        var ck_slot7 = $("#slot-7").attr('class');
        console.log("ck_slot7" + ck_slot7);
        var ck_slot8 = $("#slot-8").attr('class');
        console.log("ck_slot8" + ck_slot8);


        if (ck_slot1 == "col-sm-3 default" || ck_slot1 == "col-sm-3 failed" || ck_slot1 == "col-sm-3 passes") {
            sessionStorage.removeItem('slot_abort1');
        } else {
            sessionStorage.getItem("slot_abort1");
        }

        if (ck_slot2 == "col-sm-3 default" || ck_slot2 == "col-sm-3 failed" || ck_slot2 == "col-sm-3 passes") {
            sessionStorage.removeItem('slot_abort2');
        } else {
            sessionStorage.getItem("slot_abort2");
        }
        if (ck_slot3 == "col-sm-3 default" || ck_slot3 == "col-sm-3 failed" || ck_slot3 == "col-sm-3 passes") {
            sessionStorage.removeItem('slot_abort3');
        } else {
            sessionStorage.getItem("slot_abort3");
        }

        if (ck_slot4 == "col-sm-3 default" || ck_slot4 == "col-sm-3 failed" || ck_slot4 == "col-sm-3 passes") {
            sessionStorage.removeItem('slot_abort4');
        } else {
            sessionStorage.getItem("slot_abort4");
        }
        if (ck_slot5 == "col-sm-3 default" || ck_slot5 == "col-sm-3 failed" || ck_slot5 == "col-sm-3 passes") {
            sessionStorage.removeItem('slot_abort5');
        } else {
            sessionStorage.getItem("slot_abort5");
        }

        if (ck_slot6 == "col-sm-3 default" || ck_slot6 == "col-sm-3 failed" || ck_slot6 == "col-sm-3 passes") {
            sessionStorage.removeItem('slot_abort6');
        } else {
            sessionStorage.getItem("slot_abort6");
        }
        if (ck_slot7 == "col-sm-3 default" || ck_slot7 == "col-sm-3 failed" || ck_slot7 == "col-sm-3 passes") {
            sessionStorage.removeItem('slot_abort7');
        } else {
            sessionStorage.getItem("slot_abort7");
        }

        if (ck_slot8 == "col-sm-3 default" || ck_slot8 == "col-sm-3 failed" || ck_slot8 == "col-sm-3 passes") {
            sessionStorage.removeItem('slot_abort8');
        } else {
            sessionStorage.getItem("slot_abort8");
        }

        //disable select all checkout popup
        if ($('.checkout-slot input[type="checkbox"]').length == 0) {
            $("#all").attr('disabled', 'disabled');
        }

        //disable select all abort popup
        if ($('.abort-slot input[type="checkbox"]').length == 0) {
            $("#all-abort").attr('disabled', 'disabled');
        }

        console.log("slot_abort1" + sessionStorage.getItem("slot_abort1"));
        console.log("slot_abort2" + sessionStorage.getItem("slot_abort2"));
        console.log("slot_abort3" + sessionStorage.getItem("slot_abort3"));
        console.log("slot_abort4" + sessionStorage.getItem("slot_abort4"));
        console.log("slot_abort5" + sessionStorage.getItem("slot_abort5"));
        console.log("slot_abort6" + sessionStorage.getItem("slot_abort6"));
        console.log("slot_abort7" + sessionStorage.getItem("slot_abort7"));
        console.log("slot_abort8" + sessionStorage.getItem("slot_abort8"));

        if (sessionStorage.getItem("slot_abort1") == 1) {
            $("#box" + sessionStorage.getItem("slot_abort1")).attr('disabled', true);
            $("#box" + sessionStorage.getItem("slot_abort1")).prop('checked', false);
        }
        if (sessionStorage.getItem("slot_abort2") == 2) {
            $("#box" + sessionStorage.getItem("slot_abort2")).attr('disabled', true);
            $("#box" + sessionStorage.getItem("slot_abort2")).prop('checked', false);
        }
        if (sessionStorage.getItem("slot_abort3") == 3) {
            $("#box" + sessionStorage.getItem("slot_abort3")).attr('disabled', true);
            $("#box" + sessionStorage.getItem("slot_abort3")).prop('checked', false);
        }
        if (sessionStorage.getItem("slot_abort4") == 4) {
            $("#box" + sessionStorage.getItem("slot_abort4")).attr('disabled', true);
            $("#box" + sessionStorage.getItem("slot_abort4")).prop('checked', false);
        }
        if (sessionStorage.getItem("slot_abort5") == 5) {
            $("#box" + sessionStorage.getItem("slot_abort5")).attr('disabled', true);
            $("#box" + sessionStorage.getItem("slot_abort5")).prop('checked', false);
        }
        if (sessionStorage.getItem("slot_abort6") == 6) {
            $("#box" + sessionStorage.getItem("slot_abort6")).attr('disabled', true);
            $("#box" + sessionStorage.getItem("slot_abort6")).prop('checked', false);
        }
        if (sessionStorage.getItem("slot_abort7") == 7) {
            $("#box" + sessionStorage.getItem("slot_abort7")).attr('disabled', true);
            $("#box" + sessionStorage.getItem("slot_abort7")).prop('checked', false);
        }
        if (sessionStorage.getItem("slot_abort8") == 8) {
            $("#box" + sessionStorage.getItem("slot_abort8")).attr('disabled', true);
            $("#box" + sessionStorage.getItem("slot_abort8")).prop('checked', false);
        }
    });

});

function openScanIn() {
    $("#batchModal").modal('show')
    $('.logop').find('option[value=' + chassis_name + ']').attr('selected', 'selected');

}

function openScanInSubSlot() {
    $("#batchModalSubSlot").modal('show')
    $('.logop').find('option[value=' + chassis_name + ']').attr('selected', 'selected');

}

function resetVerify(slot_no) {
    if ($("#batch-col-row-" + slot_no + ".processing").length == 0) {
        $("#batch-col-row-" + slot_no).removeClass("verified verified-warning verified-failed");
        // $("#batch-col-row-" + slot_no + " input").val('');
        $("#sn" + slot_no).val('');
        $("#param" + slot_no).val('');
        $("#batch-col-row-" + slot_no + " .status-text").text('');
    }
    triggerSubmitbutton();
}

function resetVerifyChamber(slot_no) {
    if ($("#batch-col-row-chamber-" + slot_no + ".processing").length == 0) {
        $("#batch-col-row-chamber-" + slot_no).removeClass("verified verified-warning verified-failed");
        $("#batch-col-row-chamber-" + slot_no + " .status-text").text('');
    }
    triggerSubmitbutton();
}

function saveScanin() {
    var slot = $("#slot_no").val();
    console.log($("#slot-" + slot + " .slot-sn"));
    $("#slot-" + slot + " .slot-sn").text($("#serial_number").val());
}
function viewInteraction(x) {
    var slot_no = parseInt($(x).parents(".col-sm-3").attr("id").replace("slot-", ""));
    window.location.href = "./userinteraction/" + slot_no;
}
function triggerSubmitbutton() {

    $("#operation_id").on('keyup', function () {
        var textarea_value = $("#operation_id").val();
        console.log("textarea_value:" + textarea_value);
        var e = document.getElementById("testmode");
        var strUser = e.options[e.selectedIndex].value;
        console.log("strUser:" + strUser);
        if (textarea_value == '' && strUser == "Production") {
            $("#submitScanin").attr('disabled', true);
        } else {
            $("#submitScanin").removeAttr("disabled");
        }
    });

    var e1 = document.getElementById("testmode");
    var strUser1 = e1.options[e1.selectedIndex].value;
    var textarea_value1 = $("#operation_id").val();
    console.log("textarea_value1:" + textarea_value1);
    console.log("strUser1:" + strUser1);
    var verified = $(".batch-col-row .verified");
    if (verified.length > 0) {
        if (strUser1 == "Production" && textarea_value1 == '') {
            $("#submitScanin").attr("disabled", "disabled");
        } else {
            $("#submitScanin").removeAttr("disabled");
        }
    } else {
        $("#submitScanin").attr("disabled", "disabled");
    }
}
function triggerSubmitabortbtn() {
    var select = false;
    $.each($('#abortbatch .abort-slot :checkbox'), function (key, value) {

        if (value.checked) {
            select = true;
            $('#submitabortbatch').removeAttr("disabled");
            return false;
        }
        $("#submitabortbatch").attr("disabled", "disabled")


    });
}
function triggerSubmitdeliveryoutbtn() {
    var select = false;
    $.each($('#checkoutbatch .checkout-slot :checkbox'), function (key, value) {

        if (value.checked) {
            select = true;
            $('#submitdeliveryout').removeAttr("disabled");
            $('#retest').removeAttr("disabled");
            return false;
        }
        $("#submitdeliveryout").attr("disabled", "disabled")
        $("#retest").attr("disabled", "disabled")


    });
}


// verify button
function sendVerify(i) {
    var sn = $("#sn" + i).val();
    var logop = $("#logop" + i).val();
    var slot_location = $("#slot_location" + i).val();
    var robot_path = $("#code_version" + i).val();

    console.log(sn);
    console.log(i);
    if (sn != "") {
        $.ajax({
            contentType: "application/json; charset=utf-8",
            data: JSON.stringify({
                "serial_number": sn,
                "odc_type": "verify",
                "test_mode": $("#testmode").val(),
                "code_from": $("#testmode").val(),
                "operation_id": $("#operation_id").val(),
                "slot_location": slot_location,
                "test_station": test_station,
                "logop": logop,
                "chassis_name": chassis_name,
                "robot_path": robot_path
            }),
            beforeSend: function () {
                $('#myModalLoading').modal({
                    backdrop: 'static',
                    keyboard: false
                });
                setTimeout(function () {
                    $('#myModalLoading').modal('hide');
                    $('#myModal').modal('hide');
                }, 1000)
            },
            success: function (res) {
                $('#myModalLoading').modal('hide'); slot_location
                $("#batch-col-row-" + i).removeClass("verified verified-warning verified-failed");
                if (res.error) {
                    $('#myModalLoading').modal('hide');
                    $('#myModalError').modal('show');
                    $('#error_msg_modal').html(res.error);
                }
                else if (res.data.status == "OK") {
                    $('#myModalLoading').modal('hide');
                    $('#batch-col-row-' + i).addClass("verified");
                    $('#batch-col-row-' + i + " .status-text").text(res.data.error_message);
                }
                else if (res.data.status == "WARNING") {
                    $('#myModalLoading').modal('hide');
                    $('#batch-col-row-' + i + " .status-text").text(res.data.error_message);
                    $('#batch-col-row-' + i).addClass("verified-warning");
                }
                else if (res.data.status == "FAIL") {
                    $('#myModalLoading').modal('hide');
                    $('#batch-col-row-' + i + " .status-text").text(res.data.error_message);
                    $('#batch-col-row-' + i).addClass("verified-failed");
                }
                triggerSubmitbutton();
            },
            error: function (xhr, status, error) {
                $('#myModalLoading').modal('hide');
                $('#myModalError').modal('show');
                $('#error_msg_modal').html(status + " : " + error);
                console.log(error);
            },
            processData: false,
            type: 'POST',
            url: '/api/scanin'
        });
        console.log("sn:" + sn);
    }
}

// verify Chamber button
function sendVerifyChamber(i) {
    console.log("VerifyChamber");
    var sn = $("#chamber" + i).val();
    // var logop = $("#logop" + i).val();
    var slot_location = $("#chamber_location" + i).val();
    var robot_path = $("#code_version" + i).val();
    var logop = "chamber";

    console.log(sn);
    console.log(slot_location);
    if (sn != "") {
        $.ajax({
            contentType: "application/json; charset=utf-8",
            data: JSON.stringify({
                "serial_number": sn,
                "odc_type": "verify",
                "test_mode": $("#testmode").val(),
                "operation_id": $("#operation_id").val(),
                "slot_location": slot_location,
                "test_station": test_station,
                "logop": logop,
                "chassis_name": chassis_name,
                "robot_path": robot_path
            }),
            beforeSend: function () {
                $('#myModalLoading').modal({
                    backdrop: 'static',
                    keyboard: false
                });
                setTimeout(function () {
                    $('#myModalLoading').modal('hide');
                    $('#myModal').modal('hide');
                }, 1000)
            },
            success: function (res) {
                $('#myModalLoading').modal('hide'); slot_location
                $("#batch-col-row-chamber-" + i).removeClass("verified verified-warning verified-failed");
                if (res.error) {
                    $('#myModalLoading').modal('hide');

                    $('#myModalError').modal('show');
                    $('#error_msg_modal').html(res.error);
                }
                else if (res.data.status == "OK") {
                    $('#myModalLoading').modal('hide');
                    $('#batch-col-row-chamber-' + i).addClass("verified");
                    $('#batch-col-row-chamber-' + i + " .status-text").text(res.data.error_message);
                }
                else if (res.data.status == "WARNING") {
                    $('#myModalLoading').modal('hide');
                    $('#batch-col-row-chamber-' + i + " .status-text").text(res.data.error_message);
                    $('#batch-col-row-chamber-' + i).addClass("verified-warning");
                }
                else if (res.data.status == "FAIL") {
                    $('#myModalLoading').modal('hide');
                    $('#batch-col-row-chamber-' + i + " .status-text").text(res.data.error_message);
                    $('#batch-col-row-chamber-' + i).addClass("verified-failed");
                }
                triggerSubmitbutton();
            },
            error: function (xhr, status, error) {
                $('#myModalLoading').modal('hide');
                $('#myModalError').modal('show');
                $('#error_msg_modal').html(status + " : " + error);
                console.log(error);
            },
            processData: false,
            type: 'POST',
            url: '/api/scanin'
        });

        console.log("sn:" + sn);
    }
}

// verify button playbox
function sendVerify_playbox() {
    var sn = $("#serial_number").val();
    var slot_location = $("#slot_location").val();

    var dict = { "test_case": [] };
    var checked = $('.check-testcase').find('input[type="checkbox"]:checked');

    var robot_path = $("#code_version").val();

    $.each(checked, function (i, x) {
        test_case = $(x).val();
        dict.test_case[i] = test_case
    });
    console.log(dict)
    console.log(dict.test_case.length)

    if (sn != "") {
        if (dict.test_case.length > 0) {
            $.ajax({
                contentType: "application/json; charset=utf-8",
                data: JSON.stringify({
                    "serial_number": sn,
                    "odc_type": "verify",
                    "test_mode": $("#test_mode").val(),
                    "code_from": $("#code_from").val(),
                    "operation_id": $("#operation_id").val(),
                    "slot_location": slot_location,
                    "test_station": test_station,
                    "logop": $("#logop").val(),
                    "chassis_name": chassis_name,
                    "robot_path": robot_path
                }),
                beforeSend: function () {
                    $('#myModalLoading').modal({
                        backdrop: 'static',
                        keyboard: false
                    });
                    setTimeout(function () {
                        $('#myModalLoading').modal('hide');
                        $('#myModal').modal('hide');
                    }, 1000)
                },
                success: function (res) {
                    $('#myModalLoading').modal('hide');
                    // $("#batch-col-row-" + i).removeClass("verified verified-warning verified-failed");
                    console.log("Status:" + res.data.status);
                    if (res.error) {
                        $('#myModalLoading').modal('hide');
                        $('#myModalError').modal('show');
                        $('#error_msg_modal').html(res.error);
                    }
                    else if (res.data.status == "OK") {
                        $('#myModalLoading').modal('hide');
                        $("#status-respon").removeClass('hide')
                        $("#status-respon").removeClass("alert-danger");
                        $("#status-respon").addClass("alert-success");
                        $("#status-respon").text(res.data.error_message);
                        $("#submitScanin").removeAttr("disabled");
                        $('.testcase').attr('disabled', true);
                        $('.all-testcase').attr('disabled', true);
                    }
                    else if (res.data.status == "WARNING") {
                        $('#myModalLoading').modal('hide');
                        $("#status-respon").removeClass('hide')
                        $("#status-respon").removeClass("alert-success");
                        $("#status-respon").addClass("alert-danger");
                        $("#status-respon").text(res.data.error_message);
                        $("#submitScanin").attr('disabled', true);
                        $('.testcase').removeAttr("disabled");
                        $('.all-testcase').removeAttr("disabled");
                    }
                    else if (res.data.status == "FAIL") {
                        $('#myModalLoading').modal('hide');
                        $("#status-respon").removeClass('hide')
                        $("#status-respon").removeClass("alert-success");
                        $("#status-respon").addClass("alert-danger");
                        $("#status-respon").text(res.data.error_message);
                        $("#submitScanin").attr('disabled', true);
                        $('.testcase').removeAttr("disabled");
                        $('.all-testcase').removeAttr("disabled");
                    }
                    // triggerSubmitbutton();
                },
                error: function (xhr, status, error) {
                    $('#myModalLoading').modal('hide');
                    $('#myModalError').modal('show');
                    $('#error_msg_modal').html(status + " : " + error);
                    console.log(error);
                },
                processData: false,
                type: 'POST',
                url: '/api/scanin'
            });
            console.log("sn:" + sn);
        }
        else {
            $('#myModalLoading').modal('hide');
            $("#status-respon").removeClass('hide')
            $("#status-respon").removeClass("alert-success");
            $("#status-respon").addClass("alert-danger");
            $("#status-respon").text("Please check your test case");
            $("#submitScanin").attr('disabled', true);
            $('.testcase').removeAttr("disabled");
            $('.all-testcase').removeAttr("disabled");
        }
    }
}

function showStatus(i) {
    $.ajax({
        contentType: "application/json; charset=utf-8",
        beforeSend: function () {

        },
        success: function (data) {
            $("#statusModal .modal-body").empty();
            $.each(data, function (i, x) {
                $("#statusModal .modal-body").append('<div class="alert alert-info" role="alert">' + x.created + ' ' + x.status + ':' + x.message + '</div>');
            });
            console.log(data);
        },
        error: function (err) {
            console.log(err);
        },
        processData: false,
        type: 'GET',
        url: 'api/statuses/slot/' + i
    });
}

function sendDeliveryout() {
    var check_sn = $(x).parents(".col-sm-3").find(".serial_number").text();
    var uut_log_dir = $(x).parents(".col-sm-3").find(".uut_log_dir").val();
    var slot_no = parseInt($(x).parents(".col-sm-3").attr("id").replace("modal-slot-", ""));
    if (check_sn != "-" && check_sn != "") {
        var slot_location = chassis_name + slot_no
        $.ajax({
            contentType: "application/json; charset=utf-8",
            data: JSON.stringify({
                "serial_number": check_sn,
                "slot_location": slot_location,
                "uut_log_dir": uut_log_dir,
            }),
            beforeSend: function () {
                $('#myModalLoading').modal({
                    backdrop: 'static',
                    keyboard: false
                });
                setTimeout(function () {
                    $('#myModalLoading').modal('hide');
                    $('#batchModal').modal('hide');
                }, 1000)
            },
            success: function (data) {
                $('#myModalLoading').modal('hide');
                $('#batchModal').modal('hide');
                if (data.status == "OK") {
                    $('#myModalLoading').modal('hide');
                    $('#batchModal').modal('hide');

                } else {
                    var msg = '<p>' + data.error_message + '</p>'; //v.1.5
                    $('#myModalLoading').modal('hide');
                    $('#myModalError').modal('show');
                    $('#error_msg_modal').html(msg);

                    $('#batchModal').modal('hide');

                }
                if (data.status == "ERROR") {

                }
                console.log(data);
            },
            error: function (err) {
                console.log(err);
            },
            processData: false,
            type: 'POST',
            url: '/api/checkout'
        });
        console.log("sn:" + check_sn);
    }
}
function deliveryout(check_sn, slot_location, test_mode, retest, code_from, logop, uut_log_dir, slot_no, log_name, chassis_name, operation_id, batch_id, result, test_fail, test_abort, message, robot_path) {
    var format_result = "";
    if (result.length > 0)
        format_result = result[0].toUpperCase();
    return $.ajax({
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify({
            "serial_number": check_sn,
            "slot_location": slot_location,
            "uut_log_dir": uut_log_dir,
            "log_name": log_name,
            "slot_no": slot_no,
            "test_mode": test_mode,
            "retest": retest,
            "code_from": code_from,
            "logop": logop,
            "operation_id": operation_id,
            "test_station": chassis_name,
            "batch_id": batch_id,
            "result": format_result,
            "test_fail": test_fail,
            "test_abort": test_abort,
            "message_fail": message,
            "robot_path": robot_path
        }),
        beforeSend: function () {
            // console.log(data.robot_path);
            $('#myModalLoading').modal({
                backdrop: 'static',
                keyboard: false
            });
            setTimeout(function () {
                $('#myModalLoading').modal('hide');
                $('#batchModal').modal('hide');
            }, 1000)
        },
        success: function (data) {
            $('#myModalLoading').modal('hide');
            $('#batchModal').modal('hide');
            if (data.error == false) {
                $('#myModalLoading').modal('hide');
                $('#batchModal').modal('hide');
                console.log(data.data);

            } else {

                console.log(data.error);
                var msg = '<p>' + data.error + '</p>'; //v.1.5 
                $('#myModalError').modal('show');
                $('#error_msg_modal').html(msg);
            }

        },
        error: function (err) {
            var return_data = JSON.parse(err.responseText);
            if (return_data.error.length > 0) {
                var msg = '<p>' + return_data.error + '</p>';
                $('#myModalLoading').modal('hide');
                $('#myModalError').modal('show');
                $('#error_msg_modal').html(msg);
                $('#batchModal').modal('hide');
                error_msg = true;
            }
            console.log(return_data.error);
        },
        processData: false,
        type: 'POST',
        async: false,
        url: '/api/checkout'
    });
}

function sendAbortBatch() {

    var deferreds = [];
    var checked = $('#abortbatch .abort-slot').find('input[type="checkbox"]:checked');
    console.log("checked" + checked);
    var time = 1000;
    $.each(checked, function (i, x) {
        // var slot_no = parseInt($(x).parents(".checked-box").attr("id").replace("slot-", ""));
        var slot_no = $(x).parents(".checked-box").attr("id");
        var slot_location = $(x).parents(".checked-box").find(".slot_location").val();
        console.log(slot_no)
        console.log(slot_location)

        $.ajax({
            contentType: "application/json; charset=utf-8",
            data: JSON.stringify({
                "test_location": slot_location,
            }),
            beforeSend: function () {
                $('#myModalLoading').modal({
                    backdrop: 'static',
                    keyboard: false
                });
                setTimeout(function () {
                    $('#myModalLoading').modal('hide');
                    $('#batchModal').modal('hide');
                }, 1000)
            },
            success: function (data) {
                $('#myModalLoading').modal('hide');
                $('#batchModal').modal('hide');
                if (data.data.message.length > 0) {
                    $('#myModalLoading').modal('hide');
                    $('#batchModal').modal('hide');
                    var msg = '<p>' + data.data.message + '</p>';
                    $('#myModalLoading').modal('hide');
                    $('#myModalMessage').modal('show');
                    $('#msg_modal').html(msg);
                    $("#box" + slot_no).attr('disabled', true);

                    console.log(slot_no);

                    if (slot_no == 1) {
                        sessionStorage.setItem("slot_abort1", slot_no);
                        console.log(sessionStorage.getItem("slot_abort1"));
                    } else if (slot_no == 2) {
                        sessionStorage.setItem("slot_abort2", slot_no);
                        console.log(sessionStorage.getItem("slot_abort2"));
                    } else if (slot_no == 3) {
                        sessionStorage.setItem("slot_abort3", slot_no);
                        console.log(sessionStorage.getItem("slot_abort3"));
                    } else if (slot_no == 4) {
                        sessionStorage.setItem("slot_abort4", slot_no);
                        console.log(sessionStorage.getItem("slot_abort4"));
                    } else if (slot_no == 5) {
                        sessionStorage.setItem("slot_abort5", slot_no);
                        console.log(sessionStorage.getItem("slot_abort5"));
                    } else if (slot_no == 6) {
                        sessionStorage.setItem("slot_abort6", slot_no);
                        console.log(sessionStorage.getItem("slot_abort6"));
                    } else if (slot_no == 7) {
                        sessionStorage.setItem("slot_abort7", slot_no);
                        console.log(sessionStorage.getItem("slot_abort7"));
                    } else if (slot_no == 8) {
                        sessionStorage.setItem("slot_abort8", slot_no);
                        console.log(sessionStorage.getItem("slot_abort8"));
                    }

                }
                else if (data.status == "ERROR") {
                    console.log(data.status);
                }
                console.log(data);
            },
            error: function (err) {
                console.log(err);
            },
            processData: false,
            type: 'POST',
            url: '/api/abort'
        });


    });
    $.when.apply($, deferreds).then(function () {



    }).fail(function () {
        // Probably want to catch failure
    }).always(function () {
        // Or use always if you want to do the same thing
        // whether the call succeeds or fails
    });

    setTimeout(function() {
        window.location.href = window.location;
    }, 2000);
}

function sendDeliveryoutBatch() {


    var deferreds = [];
    var checked = $('#checkoutbatch .checkout-slot').find('input[type="checkbox"]:checked');
    var msg_error = false;
    var retest = false;
    $.each(checked, function (i, x) {
        console.log(x);
        var check_sn = $(x).parents(".checked-box").find(".serial_number").text();
        var uut_log_dir = $(x).parents(".checked-box").find(".uut_log_dir").val();
        var operation_id = $(x).parents(".checked-box").find(".operation_id").val();
        var batch_id = $(x).parents(".checked-box").find(".batch_id").val();
        var test_mode = $(x).parents(".checked-box").find(".test_mode").val();
        var logop = $(x).parents(".checked-box").find(".logop").val();
        var product_name = $(x).parents(".checked-box").find(".product_name").val();
        var result = $(x).parents(".checked-box").find(".result").val();
        var test_fail = $(x).parents(".checked-box").find(".test_fail").val();
        var test_abort = $(x).parents(".checked-box").find(".test_abort").val();
        var message = $(x).parents(".checked-box").find(".message").val();
        var slot_no = $(x).parents(".checked-box").attr("id");
        var slot_location = $(x).parents(".checked-box").find(".slot_location").val();
        var code_from = $(x).parents(".checked-box").find(".code_from").val();
        var datetime = uut_log_dir.split("_");
        datetime = datetime[datetime.length - 1].replace("-", "");
        var robot_path = $(x).parents(".checked-box").find(".code_version").val();
        var log_template = $(x).parents(".checked-box").find(".log_template").val();
        log_template = log_template.replace(/==station==/g, test_station);
        log_template = log_template.replace(/==sn==/g, check_sn);
        log_template = log_template.replace(/==chassis==/g, chassis_name);
        log_template = log_template.replace(/==datetime==/g, datetime);
        if (result == "passes") {
            log_template = log_template.replace(/==result==/g, "passed");
        } else {
            log_template = log_template.replace(/==result==/g, result);
        }
        log_template = log_template.replace(/==test_mode==/g, test_mode);
        log_template = log_template.replace(/==product_name==/g, product_name);
        log_template = log_template.replace(/==logop==/g, logop);
        if (check_sn != "-" && check_sn != "") {
            console.log("check_sn" + check_sn)
            deferreds.push(deliveryout(check_sn, slot_location, test_mode, retest, code_from, logop, uut_log_dir, slot_no, log_template, chassis_name, operation_id, batch_id, result, test_fail, test_abort, message, robot_path));
            console.log("sn:" + check_sn);
        }

    });
    $.when.apply($, deferreds).then(function (data, textStatus, jqXHR) {
        setTimeout(function() {
            window.location.href = window.location;
        }, 2000);
    }).fail(function () {
        console.log("fail");
        msg_error = true;
        // Probably want to catch failure
    }).always(function () {
    });
}

// submit scan in button
function sendScanin() {
    setCookie("operation_id", $("#operation_id").val(), 365);
    var deferred = $.Deferred();
    var verified = $(".batch-col-row .verified");
    var error_msg = false;
    var param = "-";
    var param_field = "option_param";
    var batch_id = getFormattedDate();

    var test_case_list = {};

    $.each(verified, function (i, x) {
        var check_sn = $(x).find(".batch-sn").val();
        console.log("sendScanin" + check_sn);
        if (param_name.length > 0) {
            param = $(x).find(".option-param").val();
            param_field = param_name.toLocaleLowerCase().replace(' ', '_');
        }
        // var slot_no = jQuery(x).attr("id").replace("batch-col-row-", "");
        var slot_no = $(x).find(".batch-slot_no").val();
        var second_param = {};
        var slot_location = $(x).find(".batch-slot_location").val();
        var robot_path = $(x).find(".batch-code_version").val();
        console.log(slot_location)
        second_param[param_field] = param;
        var get_logop = $(x).find(".logop").val();
        if (check_sn != "-" && check_sn != "") {
            var data = {
                "serial_number": check_sn,
                "test_mode": $("#testmode").val(),
                "code_from": $("#testmode").val(),
                "operation_id": $("#operation_id").val(),
                "slot_location": slot_location,
                "slot_no": slot_no,
                "batch_id": batch_id,
                "odc_type": "test",
                "sn_count": verified.length,
                "test_station": test_station,
                "second_param": second_param,
                "logop": get_logop,
                "chassis_name": chassis_name,
                "robot_path": robot_path,
                "test_case": test_case_list
            }
        
            $.ajax({
                contentType: "application/json; charset=utf-8",
                data: JSON.stringify(data),
                beforeSend: function () {
                    $('#myModalLoading').modal({
                        backdrop: 'static',
                        keyboard: false
                    });
                    setTimeout(function () {
                        $('#myModalLoading').modal('hide');
                        $('#batchModal').modal('hide');
                    }, 1000)
                },
                success: function (res) {
                    // console.log(res.data);
                    if (res.data != "") {
                        $('#myModalLoading').modal('hide');
                        $('#batchModal').modal('hide');
                    } else {
                        var msg = '<p>' + res.error + '</p>';
                        $('#myModalLoading').modal('hide');
                        $('#myModalError').modal('show');
                        $('#error_msg_modal').html(msg);
                    
                        $('#batchModal').modal('hide');
                    
                    }
                    if (res.error == "error") {
                    
                    }
                    console.log(res);
                },
                error: function (err) {
                    var return_data = JSON.parse(err.responseText);
                    if (return_data.error.length > 0) {
                        var msg = '<p>' + return_data.error + '</p>';
                        $('#myModalLoading').modal('hide');
                        $('#myModalError').modal('show');
                        $('#error_msg_modal').html(msg);
                        $('#batchModal').modal('hide');
                        error_msg = true;
                    
                    
                    }
                    console.log(return_data);
                },
                processData: false,
                type: 'POST',
                async: true,
                url: '/api/scanin'
            });
            console.log("sn:" + check_sn);
        }

    });
    // setTimeout(function () {
    //     if (!error_msg) {
    //         location.reload();
    //     }
    // }, 2000);
    // setTimeout(function(){location.reload()}, 10000);
    setTimeout(function() {
        window.location.href = window.location;
     }, 2000);


}

// retest
function ReTest() {

    var deferreds = [];
    var checked = $('#checkoutbatch .checkout-slot').find('input[type="checkbox"]:checked');

    var param = "-";
    var param_field = "option_param";
    var retest = true;

    var test_case_list = {};

    $.each(checked, function (i, x) {
        var check_sn = $(x).parents(".col-sm-3").find(".serial_number").text();
        var uut_log_dir = $(x).parents(".col-sm-3").find(".uut_log_dir").val();
        var operation_id = $(x).parents(".col-sm-3").find(".operation_id").val();
        var batch_id = $(x).parents(".col-sm-3").find(".batch_id").val();
        var test_mode = $(x).parents(".col-sm-3").find(".test_mode").val();
        var logop = $(x).parents(".col-sm-3").find(".logop").val();
        var product_name = $(x).parents(".col-sm-3").find(".product_name").val();
        var result = $(x).parents(".col-sm-3").find(".result").val();
        var test_fail = $(x).parents(".col-sm-3").find(".test_fail").val();
        var test_abort = $(x).parents(".col-sm-3").find(".test_abort").val();
        var message = $(x).parents(".col-sm-3").find(".message").val();
        var slot_no = parseInt($(x).parents(".col-sm-3").attr("id").replace("slot-", ""));
        var slot_location = $(x).parents(".col-sm-3").find(".slot_location").val();
        var code_from = $(x).parents(".col-sm-3").find(".code_from").val();
        var datetime = uut_log_dir.split("_");
        datetime = datetime[datetime.length - 1].replace("-", "");
        var robot_path = $(x).parents(".col-sm-3").find(".code_version").val();
        var log_template = $(x).parents(".col-sm-3").find(".log_template").val();
        log_template = log_template.replace(/==station==/g, test_station);
        log_template = log_template.replace(/==sn==/g, check_sn);
        log_template = log_template.replace(/==chassis==/g, chassis_name);
        log_template = log_template.replace(/==datetime==/g, datetime);
        if (result == "passes") {
            log_template = log_template.replace(/==result==/g, "passed");
        } else {
            log_template = log_template.replace(/==result==/g, result);
        }
        log_template = log_template.replace(/==test_mode==/g, test_mode);
        log_template = log_template.replace(/==product_name==/g, product_name);
        log_template = log_template.replace(/==logop==/g, logop);

        var second_param = {};
        second_param[param_field] = param;

        if (check_sn != "-" && check_sn != "") {
            console.log("check_sn" + check_sn)
            console.log("robot_path" + robot_path)
            
            deferreds.push(deliveryout(check_sn, slot_location, test_mode, retest, code_from, logop, uut_log_dir, slot_no, log_template, chassis_name, operation_id, batch_id, result, test_fail, test_abort, message, robot_path));
            var data = {
                "serial_number": check_sn,
                "test_mode": test_mode,
                "operation_id": operation_id,
                "slot_location": slot_location,
                "slot_no": slot_no,
                "batch_id": batch_id,
                "odc_type": "test",
                "sn_count": checked.length,
                "test_station": test_station,
                "second_param": second_param,
                "logop": logop,
                "chassis_name": chassis_name,
                "robot_path": robot_path,
                "test_case": test_case_list
            }
            console.log(data);
            $.ajax({
                contentType: "application/json; charset=utf-8",
                data: JSON.stringify(data),
                beforeSend: function () {
                    console.log(data.robot_path);
                    $('#myModalLoading').modal({
                        backdrop: 'static',
                        keyboard: false
                    });
                    setTimeout(function () {
                        $('#myModalLoading').modal('hide');
                        $('#batchModal').modal('hide');
                    }, 1000)
                },
                success: function (res) {
                    // console.log(res.data);
                    if (res.data != "") {
                        $('#myModalLoading').modal('hide');
                        $('#batchModal').modal('hide');
                    } else {
                        var msg = '<p>' + res.error + '</p>';
                        $('#myModalLoading').modal('hide');
                        $('#myModalError').modal('show');
                        $('#error_msg_modal').html(msg);
                        $('#batchModal').modal('hide');
                    }
                    if (res.error == "error") {
                    }
                    console.log(res);
                },
                error: function (err) {
                    var return_data = JSON.parse(err.responseText);
                    if (return_data.error.length > 0) {
                        var msg = '<p>' + return_data.error + '</p>';
                        $('#myModalLoading').modal('hide');
                        $('#myModalError').modal('show');
                        $('#error_msg_modal').html(msg);
                        $('#batchModal').modal('hide');
                        error_msg = true;
                    }
                    console.log(return_data);
                },
                processData: false,
                type: 'POST',
                async: true,
                url: '/api/scanin'
            });
            console.log("sn:" + check_sn);
        }

    });
    $.when.apply($, deferreds).then(function (data, textStatus, jqXHR) {
        location.reload();
    }).fail(function () {
        console.log("fail");
        msg_error = true;
        // Probably want to catch failure
    }).always(function () {
    });
}

function sendPlayboxBatch() {
    var batch_id = getFormattedDate();
    var slot_location = $("#slot_location").val();
    var slot_no = slot_location.replace(/^\D+/g, '');
    var param = $("#param").val();
    var robot_path = $("#code_version").val();
    var testall = false
    var param_field = "option_param";
    var second_param = {};
    second_param[param_field] = param;

    // var dict = { "test_case": [] };
    var test_case_list = {};
    var checked = $('.check-testcase').find('input[type="checkbox"]:checked');

    $.each(checked, function (i, x) {
        test_case = $(x).val();
        if (test_case == "all-testcase") {
            testall = true
            return false;
        }
        test_case_list[i] = test_case
        // dict.test_case[i] = test_case
    });
    console.log(test_case_list);

    if (testall) {
        console.log("Test-all");
        var data = {
            "serial_number": $("#serial_number").val(),
            "test_mode": $("#test_mode").val(),
            "code_from": $("#code_from").val(),
            "operation_id": $("#operation_id_playbox").val(),
            "slot_location": slot_location,
            "slot_no": slot_no,
            "batch_id": batch_id,
            "odc_type": "test",
            "sn_count": "1",
            "test_station": test_station,
            "second_param": second_param,
            "logop": $("#logop").val(),
            "chassis_name": chassis_name,
            "robot_path": robot_path,
            "test_case": test_case_list
        }
        console.log(data);
        $.ajax({
            contentType: "application/json; charset=utf-8",
            data: JSON.stringify(data),
            beforeSend: function () {
                $('#myModalLoading').modal({
                    backdrop: 'static',
                    keyboard: false
                });
                setTimeout(function () {
                    $('#myModalLoading').modal('hide');
                    $('#batchModal').modal('hide');
                }, 1000)
            },
            success: function (res) {
                // console.log(res.data);
                if (res.data != "") {
                    setTimeout(function () {
                        window.location.href = "/"
                    }, 1000)
                } else {
                    var msg = '<p>' + res.error + '</p>';
                    $('#myModalLoading').modal('hide');
                    $('#myModalError').modal('show');
                    $('#error_msg_modal').html(msg);
                    $('#batchModal').modal('hide');
                }
                if (res.error == "error") {
                }
                console.log(res);
            },
            error: function (err) {
                var return_data = JSON.parse(err.responseText);
                if (return_data.error.length > 0) {
                    var msg = '<p>' + return_data.error + '</p>';
                    $('#myModalLoading').modal('hide');
                    $('#myModalError').modal('show');
                    $('#error_msg_modal').html(msg);
                    $('#batchModal').modal('hide');
                    error_msg = true;
                }
                console.log(return_data);
            },
            processData: false,
            type: 'POST',
            async: true,
            url: '/api/scanin'
        });
    } else {
        console.log("No Test-all");
        var data = {
            "serial_number": $("#serial_number").val(),
            "test_mode": $("#test_mode").val(),
            "code_from": $("#code_from").val(),
            "operation_id": $("#operation_id_playbox").val(),
            "slot_location": slot_location,
            "slot_no": slot_no,
            "batch_id": batch_id,
            "odc_type": "test",
            "sn_count": "1",
            "test_station": test_station,
            "second_param": second_param,
            "logop": $("#logop").val(),
            "chassis_name": chassis_name,
            "robot_path": robot_path,
            "test_case": test_case_list
        }
        $.ajax({
            contentType: "application/json; charset=utf-8",
            data: JSON.stringify(data),
            beforeSend: function () {
                $('#myModalLoading').modal({
                    backdrop: 'static',
                    keyboard: false
                });
                setTimeout(function () {
                    $('#myModalLoading').modal('hide');
                    $('#batchModal').modal('hide');
                }, 1000)
            },
            success: function (res) {
                // console.log(res.data);
                if (res.data != "") {
                    setTimeout(function () {
                        window.location.href = "/"
                    }, 1000)
                } else {
                    var msg = '<p>' + res.error + '</p>';
                    $('#myModalLoading').modal('hide');
                    $('#myModalError').modal('show');
                    $('#error_msg_modal').html(msg);
                    $('#batchModal').modal('hide');
                }
                if (res.error == "error") {
                }
                console.log(res);
            },
            error: function (err) {
                var return_data = JSON.parse(err.responseText);
                if (return_data.error.length > 0) {
                    var msg = '<p>' + return_data.error + '</p>';
                    $('#myModalLoading').modal('hide');
                    $('#myModalError').modal('show');
                    $('#error_msg_modal').html(msg);
                    $('#batchModal').modal('hide');
                    error_msg = true;
                }
                console.log(return_data);
            },
            processData: false,
            type: 'POST',
            async: true,
            url: '/api/scanin'
        });
    }


}

function number2digit(n) {
    return n > 9 ? "" + n : "0" + n;
}

function setCookie(cname, cvalue, exdays) {
    var d = new Date();
    d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
    var expires = "expires=" + d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

function getFormattedDate() {
    var date = new Date().toISOString().substr(0, 19);
    var str = date.replace(/T/g, '_').replace(/-/g, '').replace(/:/g, '');

    return str;
}
