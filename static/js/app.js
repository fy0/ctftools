(function($) {
    'use strict';

    $(function() {
        var $fullText = $('.admin-fullText');
        $('#admin-fullscreen').on('click', function() {
            $.AMUI.fullscreen.toggle();
        });

        $(document).on($.AMUI.fullscreen.raw.fullscreenchange, function() {
            $fullText.text($.AMUI.fullscreen.isFullscreen ? '退出全屏' : '开启全屏');
        });

        var conn;
        var chat_items = [
            {user_id: 1, username: "位面之主", time:"", txt:"欢迎来到 ctftool 交流节点"},
        ];

        var log = function(s) {
            console.log(s);
        }

        function connect() {
            disconnect();

            var transports = [
                "websocket", "xhr-streaming", "iframe-eventsource", "iframe-htmlfile", "xhr-polling", "iframe-xhr-polling", "jsonp-polling"
            ];

            conn = new SockJS('http://' + window.location.host + '/ws/api', transports);

            log('Connecting...');

            conn.onopen = function() {
                log('Connected.');
            };

            conn.onmessage = function(e) {
                var data = JSON.parse(e.data);
                for (var i in data) {
                    var info = data[i];
                    if (info[0] == 'connect_ret') {
                        if (info[1].code == 0) {
                            for (var j in info[1].msg_log)
                                chat_items.push(info[1].msg_log[j]);
                        }
                    } else if (info[0] == 'say_ret') {
                        chat_items.push(info[1]);
                        $("#tab_talk").html("[*]交流");
                        $(".am-active > #tab_talk").html("交流");
                    }
                }
            };

            conn.onclose = function() {
                log('Disconnected.');
                conn = null;
                auto_reconnect = function() {
                    connect();
                }
                setTimeout(auto_reconnect, 5000);
            };
        };

        function disconnect() {
            if (conn != null) {
                log('Disconnecting...');

                conn.close();
                conn = null;
            }
        };

        var demo = new Vue({
            el: '#chat_box',
            data: {
                chat_items: chat_items,
            },
        })

        $('#msg_text').focus();
        $('#msg_text').keypress(function(event) {
            if (event.ctrlKey && (event.keyCode == 10 || event.keyCode == 13 ))
                $("#btn_chat_send").click();
        });

        $("#btn_chat_send").click(function() {
            var msg = $("#msg_text").val();
            if (msg.trim()) {
                conn.send(JSON.stringify([
                    ['say', msg.trim()],
                ]));
                $("#msg_text").val("");
            }
        });

        $("#tab_talk").click(function() {
            $(this).html("交流");
        })

        connect();

    });
})(jQuery);
