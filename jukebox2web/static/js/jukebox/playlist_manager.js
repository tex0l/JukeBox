jQuery(function($)
{
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

    $('.artists_col').resizable({
        handles: 'e',
        stop: relayout
    });

    $('.music_set_col').resizable({
        handles: 'w',
        stop: relayout
    });

    $('.album1').album({
        title: 'Album',
        artist: 'Artist',
        musics: [{pk: 1, title: 'Music 1', artist: 'Artist 1', number: 1},
            {pk: 2, title: 'Music 2', artist: 'Artist 2', number: 2},
            {pk: 2, title: 'Music 2', artist: 'Artist 2', number: 2},
            {pk: 2, title: 'Music 2', artist: 'Artist 2', number: 2},
            {pk: 2, title: 'Music 2', artist: 'Artist 2', number: 2},
            {pk: 2, title: 'Music 2', artist: 'Artist 2', number: 2},
            {pk: 2, title: 'Music 2', artist: 'Artist 2', number: 2},
            {pk: 2, title: 'Music 2', artist: 'Artist 2', number: 2},
            {pk: 3, title: 'Music 3', artist: 'Artist 3', number: 3}]
    });

    $('.artist1').artist({
        name: 'Artist 1',
        nb_albums: 1,
        nb_musics: 1
    });

    $('.artist2').artist({
        name: 'Artist 2',
        nb_albums: 2,
        nb_musics: 10
    });

    $('.slots_list').music_set({
        slot_pairs: [{slot1_nb: 'A1', slot2_nb: 'A2', music1: $('.music1').music('option')},
            {slot1_nb: 'A3', slot2_nb: 'A4', music1: $('.music2').music('option')},
            {slot1_nb: 'A5', slot2_nb: 'A6', music2: $('.music3').music('option')}]
    });

    $(".slot_left" ).droppable({
        drop: function( event, ui ) {
            $(this).parent().music_slot_pair('option', 'music1', ui.draggable.music('option'));
            $(this).find('.music_slot').addClass('music_modified');
        },
        hoverClass: "music_highlight"
    });

    $(".slot_right" ).droppable({
        drop: function( event, ui ) {
            $(this).parent().music_slot_pair('option', 'music2', ui.draggable.music('option'));
            $(this).find('.music_slot').addClass('music_modified');
        },
        hoverClass: "music_highlight"
    });

    $(".set_select").change(function(){
        $("#selected_set").find('a').html($(this).find(':selected').text());
    });

    $("#search_input").keyup(function(e){
        $("#search_string").find('span').html($(this).val());
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
});
