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

            this.music_artwork = $('<aside>')
                .addClass("music_artwork hide_in_lib")
                .append($('<img src="' + this.options.artwork + '" alt="Album Artwork" height="80" width="80">'))
                .appendTo( this.element );

            this.music_infos = $('<div>')
                .addClass("music_infos");

            $('<div>').addClass("music_number hide_in_drag")
                .html(this.options.number)
                .appendTo( this.music_infos );

            $('<div>').addClass("music_title")
                .html(this.options.title)
                .appendTo( this.music_infos );

            $('<div>').addClass("music_length hide_in_drag")
                .html(this.options.length)
                .appendTo( this.music_infos );

            $('<div>').addClass("music_artist hide_in_lib")
                .html(this.options.artist)
                .appendTo( this.music_infos );

            $('<div>').addClass("music_album hide_in_lib")
                .html(this.options.album)
                .appendTo( this.music_infos );

            this.music_infos.appendTo(this.element)

            this._refresh();
        },

        // called when created, and later when changing options
        _refresh: function() {

        },

        // events bound via _on are removed automatically
        // revert other modifications here
        _destroy: function() {
            // remove generated elements
            this.music_artwork.remove();
            this.music_infos.remove();

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
});