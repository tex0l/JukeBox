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

    $( ".playlist_slot" ).droppable({
        drop: function( event, ui ) {
            var music = ui.draggable.music('option','title');
            $( this )
                .addClass( "ui-state-highlight" )
                .find( "p" )
                .html( music );
        },
        hoverClass: "music_slot_hoovered"
    });

    $('.music1').music({
        title: 'Musicc music music music music music 1',
        number: 1,
        length: '00:00'
    });

    $('.music2').music({
        title: 'Music 2',
        number: 2
    });

    $('.music3').music({
        title: 'Music 3',
        number: 30
    });

});
