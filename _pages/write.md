---
layout: page
title: Write
permalink: /write/
published: true
---

<!-- Include Quill stylesheet -->
<link href="https://cdn.quilljs.com/1.0.0/quill.snow.css" rel="stylesheet">

<!-- Create the editor container -->
<div id="editor">
  <p>Hello World!</p>
</div>

<!-- Include the Quill library -->
<script src="https://cdn.quilljs.com/1.0.0/quill.js"></script>

<!-- Initialize Quill editor -->
<script>
  var editor = new Quill('#editor', {
    theme: 'snow'
  });
</script>

<!-- <link href="https://cdnjs.cloudflare.com/ajax/libs/trix/1.2.1/trix.css" rel="stylesheet">
<script src="https://cdnjs.cloudflare.com/ajax/libs/trix/1.2.1/trix.js"></script> -->
<!-- Place an empty <trix-editor></trix-editor> -->

<title>How to Convert Hindi Text into English Using JavaScript?</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
<script type="text/javascript" src="http://www.google.com/jsapi"></script>
<link href="http://www.google.com/uds/modules/elements/transliteration/api.css"
type="text/css" rel="stylesheet"/>


<div id="Wrapper"> <h2> Write Hindi! </h2>
<textarea id="transliterateTextarea2" style="width:650px;height:300px"></textarea>
</div>

<script type="text/javascript">
// Load the Google Transliteration API
google.load("elements", "1", {
  packages: "transliteration"
});
function onLoad() {
  var options = {
    sourceLanguage:
    google.elements.transliteration.LanguageCode.ENGLISH,
    destinationLanguage:
    google.elements.transliteration.LanguageCode.HINDI,
    shortcutKey: 'ctrl+g',
    transliterationEnabled: true
  };
  var control = new google.elements.transliteration.TransliterationControl(options);
  control.makeTransliteratable(['transliterateTextarea2']);
}
google.setOnLoadCallback(onLoad);
</script>
