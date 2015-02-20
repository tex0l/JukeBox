$(function() {

    $.widget( "juke.music", {
        // default options
        options: {
            pk: 0,
            number: 0,
            title: 'Title',
            artist: 'Artist',
            album: 'Album',
            artwork: '/media/Library/Im_Shipping_Up_to_Boston.jpg',
            length: '0:00',

            // callbacks
            change: null,
            random: null
        },

        // the constructor
        _create: function() {

            this.artist_artwork = $('<aside>')
                .addClass("music_artwork hide_in_lib")
                .append($('<img src="' + this.options.artwork + '" alt="' + this.options.title + '" height="70" width="70">'))
                .appendTo( this.element );

            this.artist_infos = $('<div>')
                .addClass("music_infos");

            $('<aside>').addClass("music_number hide_in_drag")
                .html(this.options.number)
                .appendTo( this.artist_infos );

            $('<aside>').addClass("music_length hide_in_drag")
                .html(this.options.length)
                .appendTo( this.artist_infos );

            $('<div>').addClass("music_title")
                .html(this.options.title)
                .appendTo( this.artist_infos );

            $('<div>').addClass("music_artist hide_in_lib")
                .html(this.options.artist)
                .appendTo( this.artist_infos );

            $('<div>').addClass("music_album hide_in_lib")
                .html(this.options.album)
                .appendTo( this.artist_infos );

            this.artist_infos.appendTo(this.element)

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
            nb_albums: 0,
            nb_musics: 0,
            artwork: '/media/Library/Im_Shipping_Up_to_Boston.jpg',

            // callbacks
            change: null,
            random: null
        },

        // the constructor
        _create: function() {

            var artist = this.element;

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

            artist.addClass('artist').click(function(){
                artist.addClass('artist_selected');
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

});