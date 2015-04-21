jQuery(function($)
{

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            function getCookie(name) {
                var cookieValue = null;
                if (document.cookie && document.cookie != '') {
                    var cookies = document.cookie.split(';');
                    for (var i = 0; i < cookies.length; i++) {
                        var cookie = jQuery.trim(cookies[i]);
                        // Does this cookie string begin with the name we want?
                        if (cookie.substring(0, name.length + 1) == (name + '=')) {
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                            break;
                        }
                    }
                }
                return cookieValue;
            }
            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                // Only send the token to relative URLs i.e. locally.
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        }
    });

    var container = $('.page_layout');
    var library_layout = $('.library_layout');
    var album_viewer = $('.album_viewer');
    var albums_list = $('.albums_list');
    var album_musics = $('.album_musics');
    var album_artwork = $('.album_artwork');

    function relayout() {
        album_viewer = $('.album_viewer');
        album_musics = $('.album_musics');
        album_artwork = $('.album_artwork');
        container.layout({resize: false});
        library_layout.layout({resize: false});
        var width_library_col = $('.library_col').width();
        var library_musics = $('.library_music');
        if(width_library_col > 750){
            library_musics.height(20);
            album_musics.layout({resize: true, columns: 2});
            album_musics.width('calc(100% - 200px)');
            album_musics.layout({resize: false, columns: 2});
        }
        else{
            library_musics.height(20);
            album_musics.layout({resize: true, columns: 1});
            album_musics.width('calc(100% - 200px)');
            album_musics.layout({resize: false, columns: 1});
        }
    }
    relayout();

    $(window).resize(relayout);

    var lib_json = $.getJSON('ajax/library', function(data){
        $('.library_layout').library(data);
    });

    $('.artists_col').resizable({
        handles: 'e',
        stop: relayout
    });

    $('.music_set_col').resizable({
        handles: 'w',
        stop: relayout
    });

    /*$('<div>').music_set({
     slot_pairs: [{slot1_nb: 'A1', slot2_nb: 'A2'},
     {slot1_nb: 'A3', slot2_nb: 'A4'},
     {slot1_nb: 'A5', slot2_nb: 'A6'},
     {slot1_nb: 'A7', slot2_nb: 'A8'},
     {slot1_nb: 'A9', slot2_nb: 'A10'},
     {slot1_nb: 'A11', slot2_nb: 'A12'},
     {slot1_nb: 'A13', slot2_nb: 'A14'},
     {slot1_nb: 'A15', slot2_nb: 'A16'},
     {slot1_nb: 'A17', slot2_nb: 'A18'},
     {slot1_nb: 'A19', slot2_nb: 'A20'}]
     }).appendTo('.slots_list');*/

            $.getJSON('ajax/sets', function(data){
        console.log(data)
        $('.slots_list').music_sets_list(data);
    });

    $(".slot_left" ).droppable({
        drop: function( event, ui ) {
            var m = ui.draggable.music('option');
            m.modified = true;
            $(this).parent().music_slot_pair('option', 'music1', m);
        },
        hoverClass: "music_highlight"
    });

    $(".slot_right" ).droppable({
        drop: function( event, ui ) {
            var m = ui.draggable.music('option');
            m.modified = true;
            $(this).parent().music_slot_pair('option', 'music2', m);
        },
        hoverClass: "music_highlight"
    });

    $("#set_select").change(function(){
        $("#selected_set").find('a').html($(this).find(':selected').attr('value'));
        $('.music_set').hide();
        $('.music_set_' + $(this).find(':selected').attr('value')).show();
    });

    $("#search_input").keyup(function(e){
        var search = $(this).val().toLowerCase();
        $("#search_string").find('span').html(search);
        var lib = $('.library_layout');
        lib.find('.library_artist').hide();
        lib.find('.album_viewer').hide();
        lib.find('.library_music').css({opacity : 0.15}).draggable('disable');
        var artists = lib.library('option', 'artists');
        for (var i in artists){
            var albums = artists[i].albums;
            for (var j in albums){
                var musics = albums[j].musics;
                for (var k in musics){
                    if (musics[k].title.toLowerCase().indexOf(search) > -1 ||
                        musics[k].album.toLowerCase().indexOf(search) > -1 ||
                        musics[k].artist.toLowerCase().indexOf(search) > -1 ){
                        lib.find('.music_' + musics[k].pk).css({opacity : 1}).draggable('enable');
                        lib.find('.album_' + albums[j].pk).show();
                        lib.find('.lib_artist_' + artists[i].pk).show();
                    }
                }
                if (albums[j].title.toLowerCase().indexOf(search) > -1){
                    lib.find('.album_' + albums[j].pk).show()
                        .find('.library_music').css({opacity : 1}).draggable('enable');
                    lib.find('.lib_artist_' + artists[i].pk).show();
                }
            }
            if (artists[i].name.toLowerCase().indexOf(search) > -1){
                lib.find('.lib_artist_' + artists[i].pk).show()
                    .find('.album_viewer').show()
                    .find('.library_music').css({opacity : 1}).draggable('enable');
            }
        }
        $(window).resize();
        if(e.keyCode == 13) {
            $("#search_input").blur();
        }
    });

    $("#search_label").focusin(function(){
        $(this).parent().addClass("searchform_enabled");
    });

    $("#search_label").focusout(function(){
        $(this).parent().removeClass("searchform_enabled");
    });

    $(".styled-select").attr('select_button', "\uf078");

    $(".styled-select").focusin(function(){
        $(this).addClass("styled-select_active");
    });

    $(".styled-select").focusout(function(){
        $(this).removeClass("styled-select_active");
    });

    $("#btn_edit").click(function(){
        var select = $('#set_select');
        if(select.is(":visible")) {
            select.hide();
            var old_button = select.parent().attr('select_button');
            select.parent().attr('select_button', '');

            var select_input = $('<input class="set_select set_input">')
                .val(select.find(':selected').text())
                .appendTo(select.parent());

            var btn_revert = $('<a href="#" class="btn" id="btn_revert" title="Discard changes">')
                .html('<i class="fa fa-reply"></i>')
                .appendTo(select.parent())
                .click(function () {
                    select_input.val(select.find(':selected').text());
                    end_input();
                });

            var btn_remove = $('<a href="#" class="btn" id="btn_remove" title="Delete Music Set">')
                .html('<i class="fa fa-remove"></i>')
                .appendTo(select.parent())
                .click(function () {
                    select.find(':selected').remove();
                    end_input();
                });

            var end_input = function () {
                select_input.blur();
                select_input.remove();
                btn_revert.remove();
                btn_remove.remove();
                select.parent().attr('select_button', old_button);
                select.show().change();
            };

            select_input.keypress(function (e) {
                if (e.keyCode == 13) {
                    select.find(':selected').html($(this).val());
                    end_input();
                }
            }).focus();
        }
        else{
            $('.set_input').focus();
        }
    });

    $("#btn_add").click(function(){
        $('#add_music_set_dialog').dialog('open');
    });

    $("#btn_playlist_editor").click(function(){
        var sets = $('.slots_list').music_sets_list('option', 'sets');
        $('#playlist_editor_dialog').playlist_editor({'sets': sets}).dialog('open');
    });

    $("#btn_save").click(function(){
        $.ajax({
            type: "POST",
            url: "ajax/sets",
            data: {'type': 'save', 'sets': JSON.stringify($('.slots_list').music_sets_list('get_list'))},
            dataType: 'json',
            success: function(response) {
                console.log("Music Sets saved !!!");
            }
        });
    });

    $.contextMenu({
        selector: '.music:not(.music_empty)',
        items: {
            "edit": {name: "Edit", icon: "edit", callback: function() {
                $('#edit_music_dialog').music_edit($(this).music('option')).dialog('open');
            }},
            "play": {name: "Play", icon: "play", callback: function() {
                var d = $('#play_music_dialog');
                var a = d.find('audio');
                a.attr('src', $(this).music('option', 'url'));
                d.dialog('open');
                setTimeout( function () {
                    console.log("starting play !");
                    $('#player')[0].play();
                }, 500);
            }}
        },
        events: {
            show: function(){
                $('.music').removeClass('music_selected');
                $(this).addClass('music_selected');
            }
        }
    });

    $.contextMenu({
        selector: '.artist',
        items: {
            "edit_artwork": {name: "Edit Artist Artwork", icon: "edit", callback: function() {
                $.getJSON('ajax/artwork', {'type': 'artist', 'pk': $(this).artist('option', 'pk')}, function(data){
                    console.log(data);
                    var d = $('#artist_artwork_dialog');
                    d.artist_artwork_edit(data);
                    d.dialog('open');
                });
            }}
        }
    });

    $.contextMenu({
        selector: '.album_viewer',
        items: {
            "edit_artwork": {name: "Edit Album Artwork", icon: "edit", callback: function() {
                $.getJSON('ajax/artwork', {'type': 'album', 'pk': $(this).album('option', 'pk')}, function(data){
                    console.log(data);
                    var d = $('#album_artwork_dialog');
                    d.album_artwork_edit(data);
                    d.dialog('open');
                });
            }}
        }
    });

    var add_music_set = function() {
        var e = '#add_music_set_dialog'
        $.ajax({
            type: "POST",
            url: "ajax/sets",
            data: {'type': 'add', 'name': $(e).find('input').val()},
            dataType: 'json',
            success: function(response) {
                $('<option value="' + response.pk + '" selected="selected">').html(response.name)
                    .appendTo('#set_select');
                $('.music_set').hide();
                $('<div class="music_set_' + response.pk + '">')
                    .music_set(response).appendTo('.slots_list');

            }
        });
        $(e).find('input').val('');
        $(e).dialog('close');
    };

    $('#add_music_set_dialog').dialog({
        autoOpen: false,
        show: {
            effect: "blind",
            duration: 300
        },
        hide: {
            effect: "blind",
            duration: 300
        },
        modal: true,
        buttons: {
            "Add Music Set":add_music_set,
            Cancel: function() {
                $(this).dialog('close');
            }
        },
        width: 400
    }).find('input').keyup(function(e){
        if(e.keyCode == 13) {
            add_music_set();
        }
    });

    $('#playlist_editor_dialog').dialog({
        autoOpen: false,
        show: {
            effect: "blind",
            duration: 300
        },
        hide: {
            effect: "blind",
            duration: 300
        },
        modal: true,
        buttons: {
            "Print Labels": function(){

            },
            "Push to JukeBox": function(){
                var t = $(this);
                var a = t.find("#select_A").val();
                var b = t.find("#select_B").val();
                var c = t.find("#select_C").val();
                var d = t.find("#select_D").val();
                $.ajax({
                    type: "POST",
                    url: "ajax/sets",
                    data: {'type': 'save', 'sets': JSON.stringify($('.slots_list').music_sets_list('get_list'))},
                    dataType: 'text',
                    success: function() {
                        console.log("Sets saved... Saving selected ones")
                        $.ajax({
                            type: "POST",
                            url: "ajax/sets",
                            data: {'type': 'select', 'A': a, 'B': b, 'C': c, 'D': d},
                            dataType: 'json',
                            success: function() {
                                t.dialog('close');
                            }
                        });
                    }
                });
            },
            "Push to JukeBox & Print Labels": function(){
                var t = $(this);
                var a = t.find("#select_A").val();
                var b = t.find("#select_B").val();
                var c = t.find("#select_C").val();
                var d = t.find("#select_D").val();
                $.ajax({
                    type: "POST",
                    url: "ajax/sets",
                    data: {'type': 'select', 'A': a, 'B': b, 'C': c, 'D': d},
                    dataType: 'json',
                    success: function() {
                        t.dialog('close');
                    }
                });
            },
            Cancel: function() {
                $(this).dialog('close');
            }
        },
        width: 400
    }).find('input').keyup(function(e){
        if(e.keyCode == 13) {
            add_music_set();
        }
    });

    $('#edit_music_dialog').dialog({
        autoOpen: false,
        show: {
            effect: "blind",
            duration: 300
        },
        hide: {
            effect: "blind",
            duration: 300
        },
        modal: true,
        buttons: {
            "Save Changes": function() {
                $(this).find('.submit_music_edit_btn').click();
            },
            Cancel: function() {
                $(this).dialog('close');
            }
        },
        width: 400
    }).css({overflow: 'visible'});

    $('#play_music_dialog').dialog({
        autoOpen: false,
        show: {
            effect: "blind",
            duration: 300
        },
        hide: {
            effect: "blind",
            duration: 300
        },
        modal: true,
        buttons: {},
        width: 'auto',
        height: 'auto'
    });

    $('#artist_artwork_dialog').dialog({
        autoOpen: false,
        show: {
            effect: "blind",
            duration: 300
        },
        hide: {
            effect: "blind",
            duration: 300
        },
        modal: true,
        buttons: {
            "Save Changes": function() {
                console.log('Saving chosen artwork');
                $(this).find('.submit_artist_artwork_btn').click();
            },
            Cancel: function() {
                $(this).dialog('close');
            }
        },
        width: '80%',
        height: 500
    });

    $('#album_artwork_dialog').dialog({
        autoOpen: false,
        show: {
            effect: "blind",
            duration: 300
        },
        hide: {
            effect: "blind",
            duration: 300
        },
        modal: true,
        buttons: {
            "Save Changes": function() {
                console.log('Saving chosen artwork');
                $(this).find('.submit_album_artwork_btn').click();
            },
            Cancel: function() {
                $(this).dialog('close');
            }
        },
        width: '80%',
        height: 500
    });

    $('#uploader').find('#id_file_field').fileupload({
        url: 'ajax/upload',
        dataType: 'json',
        done: function (e, data) {
            var scroll = $('.library_col').scrollTop();
            $('.library_layout').library(data.result);
            $('.library_col').scrollTop(scroll);
        },
        progressall: function (e, data) {
            var progress = parseInt(data.loaded / data.total * 100, 10);
            //$('#progress .progress-bar').css(
            //    'width',
            //    progress + '%'
            //);
            console.log(progress);
        }
    }).prop('disabled', !$.support.fileInput)
        .parent().addClass($.support.fileInput ? undefined : 'disabled');
});
