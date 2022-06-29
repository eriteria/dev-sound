/**
 * @license Copyright (c) 2003-2021, CKSource - Frederico Knabben. All rights reserved.
 * For licensing, see https://ckeditor.com/legal/ckeditor-oss-license
 */

CKEDITOR.editorConfig = function( config ) {
	// Define changes to default configuration here. For example:
	// config.language = 'fr';
	// config.uiColor = '#AADC6E';
};
CKEDITOR.on('instanceReady', function (ev) {
   ev.editor.dataProcessor.htmlFilter.addRules(
    {
       elements:
        {
          $: function (element) {
            // check for the tag name
            if (element.name == 'img') {

                element.attributes.class = "mb-sm-5 mb-grid-gutter rounded" // Put your class name here
            }
            if (element.name == 'p'){
                element.attributes.class = "mb-sm-5 h5 mb-grid-gutter"
            }

            // return element with class attribute
            return element;
         }
       }
   });
 });