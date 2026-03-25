$(document).ready(function () {

    // Call Python init function
    eel.init();

    // Text animation
    $('.text').textillate({
        loop: true,
        sync: true,
        in: {
            effect: "bounceIn",
        },
        out: {
            effect: "bounceOut",
        },
    });

    // Siri wave animation
    var siriWave = new SiriWave({
        container: document.getElementById("siri-container"),
        width: 800,
        height: 200,
        style: "ios9",
        amplitude: 1,
        speed: 0.30,
        autostart: true
    });

    // Siri message animation
    $('.siri-message').textillate({
        loop: true,
        sync: true,
        in: {
            effect: "fadeInUp",
            sync: true,
        },
        out: {
            effect: "fadeOutUp",
            sync: true,
        },
    });

    // Mic button click
    $("#MicBtn").click(function () {
        eel.playAssistantSound();
        $("#Oval").attr("hidden", true);
        $("#SiriWave").attr("hidden", false);
        eel.allCommands()();
    });

    // Keyboard shortcut (Win + J)
    function doc_keyUp(e) {
        if (e.key === 'j' && e.metaKey) {
            eel.playAssistantSound();
            $("#Oval").attr("hidden", true);
            $("#SiriWave").attr("hidden", false);
            eel.allCommands()();
        }
    }

    document.addEventListener('keyup', doc_keyUp, false);

    // Send message manually
    function PlayAssistant(message) {

        if (message != "") {

            $("#Oval").attr("hidden", true);
            $("#SiriWave").attr("hidden", false);

            eel.allCommands(message);

            $("#chatbox").val("");

            $("#MicBtn").attr('hidden', false);
            $("#SendBtn").attr('hidden', true);
        }
    }

    // Toggle mic/send button
    function ShowHideButton(message) {

        if (message.length == 0) {
            $("#MicBtn").attr('hidden', false);
            $("#SendBtn").attr('hidden', true);
        }
        else {
            $("#MicBtn").attr('hidden', true);
            $("#SendBtn").attr('hidden', false);
        }
    }

    // Text input typing
    $("#chatbox").keyup(function () {

        let message = $("#chatbox").val();

        ShowHideButton(message);

    });

    // Send button
    $("#SendBtn").click(function () {

        let message = $("#chatbox").val();

        PlayAssistant(message);

    });

    // Enter key send
    $("#chatbox").keypress(function (e) {

        key = e.which;

        if (key == 13) {

            let message = $("#chatbox").val();

            PlayAssistant(message);
        }
    });

});