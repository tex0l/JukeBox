$(function() {

    $.widget( "juke.music", {
        // default options
        options: {
            pk: 0,
            number: 0,
            disc_nb: 0,
            title: 'Empty',
            artist: '',
            album_artist: '',
            album: '',
            artwork: 'http://www.vgmpf.com/Wiki/images/3/37/Tetris_-_NES_-_Album_Art.jpg',
            artwork_pk: 0,
            length: '0:00',
            slot: '00',
            modified: false,

            // callbacks
            change: null,
            random: null
        },

        // the constructor
        _create: function() {
            this._refresh();
        },

        // called when created, and later when changing options
        _refresh: function() {

            if(this.options.pk == 0) {
                this.element.addClass('music_empty');
            } else {
                this.element.removeClass('music_empty');
            }

            this.element.removeClass('music_modified');
            if(this.options.modified){
                this.element.addClass('music_modified');
            }

            this.element.html('');

            this.artist_artwork = $('<aside>')
                .addClass("music_artwork hide_in_lib hide_in_slot")
                .append($('<img src="' + this.options.artwork + '" alt="' + this.options.title + '" height="70" width="70">'))
                .appendTo( this.element );

            this.artist_infos = $('<div>')
                .addClass("music_infos");

            $('<aside>').addClass("music_number hide_in_drag hide_in_slot")
                .html((this.options.number) ? this.options.number : '&nbsp;' )
                .appendTo( this.artist_infos );

            $('<aside>').addClass("music_length hide_in_drag hide_in_slot")
                .html(this.options.length)
                .appendTo( this.artist_infos );

            $('<div>').addClass("music_slot_nb hide_in_drag hide_in_lib")
                .html(this.options.slot)
                .appendTo( this.artist_infos );

            $('<div>').addClass("music_title")
                .html(this.options.title)
                .appendTo( this.artist_infos );

            $('<div>').addClass("music_artist hide_in_lib")
                .html(this.options.artist)
                .appendTo( this.artist_infos );

            $('<div>').addClass("music_album hide_in_lib hide_in_slot")
                .html(this.options.album)
                .appendTo( this.artist_infos );

            this.artist_infos.appendTo(this.element);

            this.element.addClass('music music_' + this.options.pk)
                .draggable({
                    revert: 'invalid',
                    helper: function() {
                        return $('<div>').music($(this).music("option")).addClass("dragged_music");
                    },
                    start: function() {
                        $('.music').removeClass('music_selected');
                        $(this).addClass("music_selected");
                    },
                    appendTo: $('.page_layout'),
                    scroll: false,
                    zIndex: 100,
                    cursorAt: { top:40, left: 130 },
                    disabled: false
                })
                .click(function(){
                    $('.music').removeClass('music_selected');
                    $(this).addClass("music_selected");
                });

            if(this.options.pk == 0) {
                this.element.draggable('option','disabled',true);
            }
        },

        // events bound via _on are removed automatically
        // revert other modifications here
        _destroy: function() {
            // remove generated elements
            this.artist_artwork.remove();
            this.artist_infos.remove();

            this.element
                .removeClass( "dragged_music" )
                .css( "background-color", "transparent" );
        },

        // _setOptions is called with a hash of all options that are changing
        // always refresh when changing options
        _setOptions: function() {
            // _super and _superApply handle keeping the right this-context
            this._superApply( arguments );
            this._refresh();
        },

        // _setOption is called for each individual option that is changing
        _setOption: function( key, value ) {
            // prevent invalid color values
            this._super( key, value );
        }
    });

    $.widget( "juke.artist", {
        // default options
        options: {
            pk: 0,
            name: 'Artist',
            albums: [],
            nb_albums: 0,
            nb_musics: 0,
            artwork: 'http://www.vgmpf.com/Wiki/images/3/37/Tetris_-_NES_-_Album_Art.jpg',

            // callbacks
            change: null,
            random: null
        },

        // the constructor
        _create: function() {

            var artist = this.element;

            this.options.nb_albums = 0;
            this.options.nb_musics = 0;

            for (var i in this.options.albums){
                this.options.nb_albums++;
                this.options.nb_musics+= this.options.albums[i].musics.length;
            }

            this.artist_artwork = $('<aside>')
                .addClass("artist_artwork")
                .append($('<img src="' + this.options.artwork + '" alt="' + this.options.name + '" height="70" width="70">'))
                .appendTo( artist );

            this.artist_infos = $('<div>')
                .addClass("artist_infos");

            $('<div>').addClass("artist_name")
                .html(this.options.name)
                .appendTo( this.artist_infos );

            this.text = ''+ this.options.nb_albums + ' album';
            if (this.options.nb_albums > 1){
                this.text+='s';
            }
            this.text+= ', ' + this.options.nb_musics + ' morceau';
            if (this.options.nb_musics > 1){
                this.text+='x';
            }

            $('<div>').addClass("artist_numbers")
                .html(this.text)
                .appendTo( this.artist_infos );

            this.artist_infos.appendTo(artist)

            artist.addClass('artist').addClass('artist_' + this.options.pk).click(function(){
                var goal = '.lib_artist_' + $(this).artist('option', 'pk') + ' > .library_artist_name';
                var speed = 750;
                $('.library_col').scrollTo( $(goal), speed, {offset: -85, axis: 'y'} );
                return false;
            });

            this._refresh();
        },

        // called when created, and later when changing options
        _refresh: function() {
        },

        // events bound via _on are removed automatically
        // revert other modifications here
        _destroy: function() {
            // remove generated elements
            this.artist_artwork.remove();
            this.artist_infos.remove();

            this.element
                .removeClass( "artist" )
                .css( "background-color", "transparent" );
        },

        // _setOptions is called with a hash of all options that are changing
        // always refresh when changing options
        _setOptions: function() {
            // _super and _superApply handle keeping the right this-context
            this._superApply( arguments );
            this._refresh();
        },

        // _setOption is called for each individual option that is changing
        _setOption: function( key, value ) {
            // prevent invalid color values
            this._super( key, value );
        }
    });

    $.widget( "juke.music_slot_pair", {
        // default options
        options: {
            pk: 0,
            slot1_nb: 'A0',
            slot2_nb: 'A0',
            music1: {},
            music2: {},
            artwork: 'http://www.vgmpf.com/Wiki/images/3/37/Tetris_-_NES_-_Album_Art.jpg',
            artwork_pk: 0,

            // callbacks
            change: null,
            random: null
        },

        // the constructor
        _create: function() {

            var slot_pair = this.element.addClass("slot_pair");

            this.options.music1.slot = this.options.slot1_nb;
            this.music_slot1 = $('<div class="music_slot">').music(this.options.music1);
            $('<aside>')
                .addClass("slot slot_left")
                .append(this.music_slot1)
                .appendTo( slot_pair )
                .droppable({
                    drop: function( event, ui ) {
                        var m = ui.draggable.music('option');
                        m.modified = true;
                        var origin = slot_pair.music_slot_pair('option', 'artwork_pk');
                        if (origin == 0 || origin == slot_pair.music_slot_pair('option', 'music1')['artwork_pk']){
                            // if there is no current artwork, or it is from the song being replaced
                            slot_pair.music_slot_pair('option', {"artwork_pk": m['artwork_pk'], 'artwork': m['artwork'] });
                        }
                        slot_pair.music_slot_pair('option', 'music1', m);
                    },
                    hoverClass: "music_highlight"
                });

            this.slot_artwork = $('<div>')
                .addClass("slot_artwork")
                .append($('<img src="' + this.options.artwork + '" height="70" width="70">'))
                .appendTo( slot_pair );

            this.options.music2.slot = this.options.slot2_nb;
            this.music_slot2 = $('<div class="music_slot">').music(this.options.music2);
            $('<aside>')
                .addClass("slot slot_right")
                .append(this.music_slot2)
                .appendTo( slot_pair )
                .droppable({
                    drop: function( event, ui ) {
                        var m = ui.draggable.music('option');
                        m.modified = true;
                        var origin = slot_pair.music_slot_pair('option', 'artwork_pk');
                        if (origin == 0 || origin == slot_pair.music_slot_pair('option', 'music2')['artwork_pk']){
                            // if there is no current artwork, or it is from the song being replaced
                            slot_pair.music_slot_pair('option', {"artwork_pk": m['artwork_pk'], 'artwork': m['artwork'] });
                        }
                        slot_pair.music_slot_pair('option', 'music2', m);
                    },
                    hoverClass: "music_highlight"
                });

        },

        // called when changing options
        _refresh: function() {
            this.options.music1.slot = this.options.slot1_nb;
            this.options.music2.slot = this.options.slot2_nb;
            this.music_slot1.music(this.options.music1);
            this.music_slot2.music(this.options.music2);
            this.slot_artwork.find('img').attr("src", this.options.artwork);
        },

        // events bound via _on are removed automatically
        // revert other modifications here
        _destroy: function() {
            // remove generated elements
        },

        // _setOptions is called with a hash of all options that are changing
        // always refresh when changing options
        _setOptions: function() {
            // _super and _superApply handle keeping the right this-context
            this._superApply( arguments );
            this._refresh();
        },

        // _setOption is called for each individual option that is changing
        _setOption: function( key, value ) {
            this._super( key, value );
        }
    });

    $.widget( "juke.music_set", {
        // default options
        options: {
            pk: 0,
            name: '',
            slot_pairs: [],

            // callbacks
            change: null,
            random: null
        },

        // the constructor
        _create: function() {
            this._refresh();
        },

        // called when created, and later when changing options
        _refresh: function() {
            this.element.addClass('music_set').find('.slot_pair').remove();

            for (var i in this.options.slot_pairs){
                $('<div>').music_slot_pair(this.options.slot_pairs[i]).appendTo(this.element);
            }
        },

        // events bound via _on are removed automatically
        // revert other modifications here
        _destroy: function() {
            // remove generated elements
        },

        // _setOptions is called with a hash of all options that are changing
        // always refresh when changing options
        _setOptions: function() {
            // _super and _superApply handle keeping the right this-context
            this._superApply( arguments );
            this._refresh();
        },

        // _setOption is called for each individual option that is changing
        _setOption: function( key, value ) {
            this._super( key, value );
        },

        get_dict: function(){
            var r ={'pk': this.options.pk, 'name': this.options.name};
            this.element.find('.slot_pair').each(function(){
                r['s' + $(this).music_slot_pair('option','slot1_nb')] = $(this).music_slot_pair('option','music1').pk;
                r['s' + $(this).music_slot_pair('option','slot2_nb')] = $(this).music_slot_pair('option','music2').pk;
                r['a' + $(this).music_slot_pair('option','slot2_nb')/2] = $(this).music_slot_pair('option', 'artwork_pk');
            });
            console.log(r);
            return r;
        }
    });

    $.widget( "juke.album", {
        // default options
        options: {
            pk: 0,
            title: '',
            artist: '',
            artwork: 'http://www.vgmpf.com/Wiki/images/3/37/Tetris_-_NES_-_Album_Art.jpg',
            musics: [],

            // callbacks
            change: null,
            random: null
        },

        // the constructor
        _create: function() {
            this.element.addClass('album_viewer').addClass('album_' + this.options.pk);

            $('<header class="album_title">')
                .html(this.options.title)
                .appendTo(this.element);

            $('<aside class="album_artwork_col">')
                .html('<img class="album_artwork" src="' + this.options.artwork
                + '" alt="'+ this.options.title + '" height="170" width="170">')
                .appendTo(this.element);

            var album_musics = $('<div data-layout=\'{"type": "grid", "hgap": 3, "vgap": 3, "fill":"vertical"}\'>')
                .addClass('album_musics');

            for (var i in this.options.musics){
                $('<div class="library_music">').music(this.options.musics[i]).appendTo(album_musics);
            }

            this.element.append(album_musics);
            $(window).resize();
        },

        // events bound via _on are removed automatically
        // revert other modifications here
        _destroy: function() {
            // remove generated elements
        },

        // _setOptions is called with a hash of all options that are changing
        // always refresh when changing options
        _setOptions: function() {
            // _super and _superApply handle keeping the right this-context
            this._superApply( arguments );
            this._refresh();
        },

        // _setOption is called for each individual option that is changing
        _setOption: function( key, value ) {
            this._super( key, value );
        }
    });

    $.widget( "juke.library_artist", {
        // default options
        options: {
            pk: 0,
            name: '',
            albums: [],

            // callbacks
            change: null,
            random: null
        },

        // the constructor
        _create: function() {
            this._refresh();
        },

        _refresh: function() {
            this.element.html('');

            this.element.addClass('library_artist')
                .addClass('lib_artist_' + this.options.pk);

            $('<div class="library_artist_name">')
                .html(this.options.name)
                .appendTo(this.element);

            for (var i in this.options.albums){
                $('<div">').album(this.options.albums[i]).appendTo(this.element);
            }
        },
        // events bound via _on are removed automatically
        // revert other modifications here
        _destroy: function() {
            // remove generated elements
        },

        // _setOptions is called with a hash of all options that are changing
        // always refresh when changing options
        _setOptions: function() {
            // _super and _superApply handle keeping the right this-context
            this._superApply( arguments );
            this._refresh();
        },

        // _setOption is called for each individual option that is changing
        _setOption: function( key, value ) {
            this._super( key, value );
        }
    });

    $.widget( "juke.artists_list", {
        // default options
        options: {
            artists: [],

            // callbacks
            change: null,
            random: null
        },

        // the constructor
        _create: function() {
            this._refresh();
        },

        _refresh: function() {
            this.element.html('');

            //TODO: Add "All Artists" button

            for (var i in this.options.artists){
                $('<a href="#">').artist(this.options.artists[i]).appendTo(this.element);
            }
        },
        // events bound via _on are removed automatically
        // revert other modifications here
        _destroy: function() {
            // remove generated elements
        },

        // _setOptions is called with a hash of all options that are changing
        // always refresh when changing options
        _setOptions: function() {
            // _super and _superApply handle keeping the right this-context
            this._superApply( arguments );
            this._refresh();
        },

        // _setOption is called for each individual option that is changing
        _setOption: function( key, value ) {
            this._super( key, value );
        }
    });

    $.widget( "juke.library", {
        // default options
        options: {
            artists: [],
            autocomplete_artists: [],
            autocomplete_albums: [],

            // callbacks
            change: null,
            random: null
        },

        // the constructor
        _create: function() {
            this._refresh();
        },

        _refresh: function() {
            var library_col = this.element.find('.library_col');
            library_col.find('.albums_list').remove();
            var albums_list = $('<div class="albums_list">').appendTo(library_col);

            for (var i in this.options.artists){
                $('<div>').library_artist(this.options.artists[i]).appendTo(albums_list);
            }

            var artists_col = this.element.find('.artists_col');
            artists_col.find('.artists_list').remove();
            var artists_container = $('<div class="artists_list">').appendTo(artists_col);
            $(window).resize();
            artists_container.artists_list({artists: this.options.artists});
        },
        // events bound via _on are removed automatically
        // revert other modifications here
        _destroy: function() {
            // remove generated elements
        },

        // _setOptions is called with a hash of all options that are changing
        // always refresh when changing options
        _setOptions: function() {
            // _super and _superApply handle keeping the right this-context
            this._superApply( arguments );
            this._refresh();
        },

        // _setOption is called for each individual option that is changing
        _setOption: function( key, value ) {
            this._super( key, value );
        }
    });

    $.widget( "juke.music_edit", {
        // default options
        options: {
            pk: 0,
            number: 0,
            disc_nb: 0,
            title: 'Empty',
            artist: '',
            album_artist : '',
            album: '',
            artwork: 'http://www.vgmpf.com/Wiki/images/3/37/Tetris_-_NES_-_Album_Art.jpg',
            length: '0:00',

            // callbacks
            change: null,
            random: null
        },

        // the constructor
        _create: function() {
            this._refresh();
        },

        // called when created, and later when changing options
        _refresh: function() {

            var lib = $('.library_layout');
            var pk = this.options.pk;

            this.element.html('');

            this.header = $('<div class="edit_header">').appendTo(this.element);

            this.artwork = $('<aside>')
                .addClass("music_artwork")
                .append($('<img src="' + this.options.artwork
                + '" alt="' + this.options.title + '" height="70" width="70">')
                    .addClass("music_artwork_img"))
                .appendTo( this.header );

            this.music_infos = $('<div>')
                .addClass("edit_music_infos")
                .appendTo( this.header );

            $('<div>').addClass("music_title")
                .html(this.options.title)
                .appendTo( this.music_infos );

            $('<div>').addClass("music_artist")
                .html(this.options.artist)
                .appendTo( this.music_infos );

            $('<div>').addClass("music_album")
                .html(this.options.album)
                .appendTo( this.music_infos );

            this.form = $('<form action="" class="edit_music_form">')
                .appendTo(this.element);

            this.fields = $('<fieldset class="edit_music_fieldset">').appendTo(this.form);

            $('<p>').append($('<label for="title">').html('Title'))
                .append($('<input type="text" name="title" id="title_music" value="' + this.options.title + '">')
                    .addClass("text ui-widget-content ui-corner-all"))
                .appendTo(this.fields);

            this.album_input = $('<input type="text" name="album" id="album" value="' + this.options.album + '">')
                .addClass("text ui-widget-content ui-corner-all");
            $('<p>').append($('<label for="album">').html('Album'))
                .append(this.album_input)
                .appendTo(this.fields);
            this.album_input.autocomplete({source: lib.library('option', 'autocomplete_albums')});

            this.artist_input = $('<input type="text" name="artist" id="artist" value="' + this.options.artist + '">')
                .addClass("text ui-widget-content ui-corner-all");
            $('<p>').append($('<label for="artist">').html('Artist'))
                .append(this.artist_input)
                .appendTo(this.fields);
            this.artist_input.autocomplete({source: lib.library('option', 'autocomplete_artists')});

            this.album_artist_input = $('<input type="text" name="album_artist" id="album_artist" value="' + this.options.album_artist + '">')
                .addClass("text ui-widget-content ui-corner-all");
            $('<p>').append($('<label for="album_artist">').html('Album Artist'))
                .append(this.album_artist_input)
                .appendTo(this.fields);
            this.album_artist_input.autocomplete({source: lib.library('option', 'autocomplete_artists')});

            $('<p>').append($('<label for="track_nb">').html('Track Number'))
                .append($('<input type="number" name="track_nb" id="track_nb" value=' + this.options.number + '>')
                    .addClass("spinner ui-widget-content ui-corner-all"))
                .append($('<label for="disc_nb">').html('Disc Number'))
                .append($('<input type="number" name="disc_nb" id="disc_nb" value=' + this.options.disc_nb + '>')
                    .addClass("spinner ui-widget-content ui-corner-all"))
                .appendTo(this.fields);

            $('<input class="submit_music_edit_btn" type="submit" tabindex="-1" style="position:absolute; top:-1000px">')
                .click(function () {
                    var title = encodeURIComponent($('input#title_music').val());
                    var album = encodeURIComponent($('input#album').val());
                    var artist = encodeURIComponent($('input#artist').val());
                    var album_artist = encodeURIComponent($('input#album_artist').val());
                    var track_nb = encodeURIComponent($('input#track_nb').val());
                    var disc_nb = encodeURIComponent($('input#disc_nb').val());
                    //var dataString = 'type=music' + '&title=' + title + '&album=' + album + '&artist=' + artist +
                    //    '&album_artist=' + album_artist + '&track_nb=' + track_nb + '&disc_nb=' + disc_nb;
                    //alert(dataString);
                    //return false;
                    var data = {'type': 'music', 'pk': pk, 'title': title, 'album': album, 'artist': artist,
                        'album_artist': album_artist, 'track_nb': track_nb, 'disc_nb': disc_nb};
                    $.ajax({
                        type: "POST",
                        url: "ajax/library",
                        data: data,
                        dataType: 'json',
                        success: function(response) {
                            var lib = $('.library_layout');
                            var scroll = $('.music_' + pk).offset().top;
                            lib.library(response);
                            var goal = $('.music_' + pk);
                            $('.library_col').scrollTo( goal, 0, {offset: -scroll, axis: 'y'} );
                            $('.music').removeClass('music_selected');
                            goal.addClass('music_selected');
                            $('#edit_music_dialog').dialog('close');
                        }
                    });
                    return false;
                })
                .appendTo(this.fields);
        },

        // events bound via _on are removed automatically
        // revert other modifications here
        _destroy: function() {
            // remove generated elements
        },

        // _setOptions is called with a hash of all options that are changing
        // always refresh when changing options
        _setOptions: function() {
            // _super and _superApply handle keeping the right this-context
            this._superApply( arguments );
            this._refresh();
        },

        // _setOption is called for each individual option that is changing
        _setOption: function( key, value ) {
            // prevent invalid color values
            this._super( key, value );
        }
    });

    $.widget( "juke.artist_artwork_edit", {
        // default options
        options: {
            pk: 0,
            name: '',
            artworks: [],
            albums: [],

            // callbacks
            change: null,
            random: null
        },

        // the constructor
        _create: function() {
            this._refresh();
        },

        // called when created, and later when changing options
        _refresh: function() {
            this.element.find('.artist_artwork_chooser').remove();

            var f = $('<form action="" class="artist_artwork_chooser">').appendTo(this.element);
            var s = $('<select class="image-picker artwork-select">').appendTo(f);
            var pk = this.options.pk;

            var artist_artworks = $('<optgroup label="Artist Artwork">').appendTo(s);
            for (var i in this.options.artworks){
                var artwork = this.options.artworks[i];
                var a = $('<option data-img-src="' + artwork.url +
                '" value="' + artwork.pk +
                '" data-img-label="' + this.options.name + '">')
                    .appendTo(artist_artworks);
                if (artwork.selected){
                    a.attr('selected', 'selected')
                }
            }
            $('<option data-img-src="/static/plus.png" value="artist_artwork_add" data-img-label="Add Artwork">')
                .appendTo(artist_artworks);

            var artist_albums_artwork = $('<optgroup label="Artist Albums">').appendTo(s);
            for (var i in this.options.albums){
                var album = this.options.albums[i];
                for (var j in album.artworks) {
                    $('<option data-img-src="' + album.artworks[j].url +
                    '" value="' + album.artworks[j].pk +
                    '" data-img-label="' + album.title +'">')
                        .appendTo(artist_albums_artwork);
                }
            }

            $('<input class="submit_artist_artwork_btn" type="submit" tabindex="-1" style="position:absolute; top:-1000px">')
                .click(function () {
                    var artwork = encodeURIComponent($('.artwork-select').val());
                    var data = {'type': 'artist', 'pk': pk, 'artwork': artwork};
                    $.ajax({
                        type: "POST",
                        url: "ajax/artwork",
                        data: data,
                        dataType: 'json',
                        success: function(response) {
                            var lib = $('.library_layout');
                            var scroll = $('.library_col').scrollTop();
                            lib.library(response);
                            $('.library_col').scrollTop( scroll );
                            $('#artist_artwork_dialog').dialog('close');
                        }
                    });
                    return false;
                })
                .appendTo(f);


            s.imagepicker({
                hide_select : true,
                show_label  : true,
                clicked: function(){
                    if (s.val()=='artist_artwork_add'){
                        $('#artist_artwork_file_field').click();
                    }
                }
            });

            this.element.find('.thumbnail').height(245).width(200);
            this.element.find('img').height(200).width(200);

            var temp = this;
            this.element.find('#artist_artwork_file_field').fileupload({
                url: 'ajax/artwork_upload',
                dropZone: this.element,
                formData: [{name: 'pk', value: this.options.pk}, {name: 'type', value: 'artist'}],
                dataType: 'json',
                done: function (e, data) {
                    temp.options.artworks.push(data.result);
                    temp._refresh();
                }
            }).prop('disabled', !$.support.fileInput)
                .parent().addClass($.support.fileInput ? undefined : 'disabled');

        },

        // events bound via _on are removed automatically
        // revert other modifications here
        _destroy: function() {
            // remove generated elements
        },

        // _setOptions is called with a hash of all options that are changing
        // always refresh when changing options
        _setOptions: function() {
            // _super and _superApply handle keeping the right this-context
            this._superApply( arguments );
            this._refresh();
        },

        // _setOption is called for each individual option that is changing
        _setOption: function( key, value ) {
            // prevent invalid color values
            this._super( key, value );
        }
    });

    $.widget( "juke.album_artwork_edit", {
        // default options
        options: {
            pk: 0,
            name: '',
            artworks: [],
            albums: [],

            // callbacks
            change: null,
            random: null
        },

        // the constructor
        _create: function() {
            this._refresh();
        },

        // called when created, and later when changing options
        _refresh: function() {
            this.element.find('.album_artwork_chooser').remove();

            var f = $('<form action="" class="album_artwork_chooser">').appendTo(this.element);
            var s = $('<select class="image-picker artwork-select">').appendTo(f);
            var pk = this.options.pk;

            var album_artworks = $('<optgroup label="Album Artwork">').appendTo(s);
            for (var i in this.options.artworks){
                var artwork = this.options.artworks[i];
                var a = $('<option data-img-src="' + artwork.url +
                '" value="' + artwork.pk +
                '" data-img-label="' + this.options.name + '">')
                    .appendTo(album_artworks);
                if (artwork.selected){
                    a.attr('selected', 'selected')
                }
            }
            $('<option data-img-src="/static/plus.png" value="album_artwork_add" data-img-label="Add Artwork">')
                .appendTo(album_artworks);


            $('<input class="submit_album_artwork_btn" type="submit" tabindex="-1" style="position:absolute; top:-1000px">')
                .click(function () {
                    var artwork = encodeURIComponent($('.artwork-select').val());
                    var data = {'type': 'album', 'pk': pk, 'artwork': artwork};
                    $.ajax({
                        type: "POST",
                        url: "ajax/artwork",
                        data: data,
                        dataType: 'json',
                        success: function(response) {
                            var lib = $('.library_layout');
                            var scroll = $('.library_col').scrollTop();
                            lib.library(response);
                            $('.library_col').scrollTop( scroll );
                            $('#album_artwork_dialog').dialog('close');
                        }
                    });
                    return false;
                })
                .appendTo(f);


            s.imagepicker({
                hide_select : true,
                show_label  : true,
                clicked: function(){
                    if (s.val()=='album_artwork_add'){
                        $('#album_artwork_file_field').click();
                    }
                }
            });

            this.element.find('.thumbnail').height(245).width(200);
            this.element.find('img').height(200).width(200);

            var temp = this;
            this.element.find('#album_artwork_file_field').fileupload({
                url: 'ajax/artwork_upload',
                dropZone: this.element,
                formData: [{name: 'pk', value: this.options.pk}, {name: 'type', value: 'album'}],
                dataType: 'json',
                done: function (e, data) {
                    temp.options.artworks.push(data.result);
                    temp._refresh();
                }
            }).prop('disabled', !$.support.fileInput)
                .parent().addClass($.support.fileInput ? undefined : 'disabled');

        },

        // events bound via _on are removed automatically
        // revert other modifications here
        _destroy: function() {
            // remove generated elements
        },

        // _setOptions is called with a hash of all options that are changing
        // always refresh when changing options
        _setOptions: function() {
            // _super and _superApply handle keeping the right this-context
            this._superApply( arguments );
            this._refresh();
        },

        // _setOption is called for each individual option that is changing
        _setOption: function( key, value ) {
            // prevent invalid color values
            this._super( key, value );
        }
    });

    $.widget( "juke.music_sets_list", {
        // default options
        options: {
            sets: [],

            // callbacks
            change: null,
            random: null
        },

        // the constructor
        _create: function() {
            this._refresh();
        },

        // called when created, and later when changing options
        _refresh: function() {
            $('#set_select').find('option').remove();
            this.element.find('.slot_pair').remove();

            var first = true;

            for (var i in this.options.sets){
                var name = this.options.sets[i].name;
                if (this.options.sets[i].selection != '') {
                    name = name + "        ||       " + this.options.sets[i].selection
                }

                $('<option value="' + this.options.sets[i].pk + '">').html(name)
                    .appendTo('#set_select');

                if (first){
                    first=false;
                    $('<div class="music_set_' + this.options.sets[i].pk + '">')
                        .music_set(this.options.sets[i]).appendTo(this.element);
                }
                else{
                    $('<div class="music_set_' + this.options.sets[i].pk + '">')
                        .music_set(this.options.sets[i]).appendTo(this.element).hide();
                }
            }
        },

        // events bound via _on are removed automatically
        // revert other modifications here
        _destroy: function() {
            // remove generated elements
        },

        // _setOptions is called with a hash of all options that are changing
        // always refresh when changing options
        _setOptions: function() {
            // _super and _superApply handle keeping the right this-context
            this._superApply( arguments );
            this._refresh();
        },

        // _setOption is called for each individual option that is changing
        _setOption: function( key, value ) {
            this._super( key, value );
        },

        get_list: function(){
            var l =[];
            this.element.find('.music_set').each(function(){
                l.push($(this).music_set('get_dict'));
            });
            console.log(l);
            return l;
        }
    });

    $.widget( "juke.playlist_editor", {
        // default options
        options: {
            sets: [],

            // callbacks
            change: null,
            random: null
        },

        // the constructor
        _create: function() {
            this._refresh();
        },

        // called when created, and later when changing options
        _refresh: function() {
            this.element.find('option').remove();

            var l = ['A', 'B', 'C', 'D'];

            for (var i in l){
                for (var j in this.options.sets){
                    var temp = $('<option value="' + this.options.sets[j].pk + '">').html(this.options.sets[j].name)
                        .appendTo('#select_'+l[i]);
                    if (this.options.sets[j].selection == l[i]){
                        temp.attr('selected', 'selected');
                    }
                }
            }
        },

        // events bound via _on are removed automatically
        // revert other modifications here
        _destroy: function() {
            // remove generated elements
        },

        // _setOptions is called with a hash of all options that are changing
        // always refresh when changing options
        _setOptions: function() {
            // _super and _superApply handle keeping the right this-context
            this._superApply( arguments );
            this._refresh();
        },

        // _setOption is called for each individual option that is changing
        _setOption: function( key, value ) {
            this._super( key, value );
        },

        get_list: function(){
            var l =[];
            this.element.find('.music_set').each(function(){
                l.push($(this).music_set('get_dict'));
            });
            console.log(l);
            return l;
        }
    });


});