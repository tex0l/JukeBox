jQuery(function($)
{
    var container = $('.page_layout');
    var album_viewer = $('.album_viewer')
    var albums_list = $('.albums_list');
    var album_musics = $('.album_musics');
    var album_artwork = $('.album_artwork');

    function relayout() {
        container.layout({resize: false});
        album_musics.height('auto');
        album_artwork.height('auto');
        var width_library_col = $('.library_col').width();
        var library_musics = $('.library_music');
        if(width_library_col > 750){
            library_musics.width((width_library_col - 234)/2);
            library_musics.height(20);
            album_musics.layout({resize: true, columns: 2});
        }
        else{
            library_musics.width(width_library_col - 218);
            library_musics.height(20);
            album_musics.layout({resize: true, columns: 1});
        }
        album_viewer.layout({resize: true});
        albums_list.layout({resize: false});
        if(width_library_col > 750){
            library_musics.height(20);
            album_musics.layout({resize: true, columns: 2});
        }
    }
    relayout();

    $(window).resize(relayout);

    $('.music_set_editor').layout({
        fill: 'vertical'
    });

    $( ".library_music" ).draggable({
        revert: 'invalid',
        helper: function() {
            return $('<div>').music($(this).music("option")).addClass("dragged_music");
        },
        appendTo: container,
        scroll: false,
        zIndex: 100,
        cursorAt: { top:40, left: 130 }
    });

    $('.artists_col').resizable({
        handles: 'e',
        stop: relayout
    });

    $('.music1').music({
        title: 'Musicc music music music music music 1',
        artist: 'Artist 1',
        number: 1,
        length: '00:00'
    });

    $('.music2').music({
        title: 'Music 2',
        artist: 'Artist 2',
        number: 2
    });

    $('.music3').music({
        title: 'Music 3',
        artist: 'Artist 3',
        number: 30
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

    $('.slot1').music_slot_pair({});

    $('.slot2').music_slot_pair({});

    $('.slot3').music_slot_pair({});

    $( ".slot" ).droppable({
        drop: function( event, ui ) {
            var music = ui.draggable.music('option');
            music.slot = $(this).find('.music_slot').html('').music('option', 'slot');
            $( this )
                .music(music);
        },
        hoverClass: "music_slot_hoovered"
    });

});
