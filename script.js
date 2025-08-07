function translateText() {
    const inputText = document.getElementById("inputText").value;
    const targetLanguage = document.getElementById("languageSelect").value;

    // Construct the Google Translate URL
    const googleTranslateUrl = `https://translate.google.com/?sl=auto&tl=${targetLanguage}&text=${encodeURIComponent(inputText)}&op=translate`;

    // Redirect to Google Translate
    window.open(googleTranslateUrl, '_blank');
}
