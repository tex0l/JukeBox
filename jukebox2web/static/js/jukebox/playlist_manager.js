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

    $('.slots_list').music_set({
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

    $(".set_select").change(function(){
        $("#selected_set").find('a').html($(this).find(':selected').text());
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
        var select = $('#set_select');
        var o = $('<option selected="selected">').appendTo(select);
        $("#btn_edit").click();
    });

    $.contextMenu({
        selector: '.library_music',
        callback: function(key, options) {
            var m = "clicked: " + key + " on " + $(this).music('option', 'title');
            window.console && console.log(m);
            $('#edit_music_dialog').music_edit($(this).music('option')).dialog('open');
        },
        items: {
            "edit": {name: "Edit", icon: "edit"}
        },
        events: {
            show: function(){
                $('.music').removeClass('music_selected');
                $(this).addClass('music_selected');
            }
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
            },
            Cancel: function() {
            }
        }
    }).css({overflow: 'visible'});
});
