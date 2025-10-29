<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>Avatar Studio — Générateur d'avatar avec voix et sous-titres</title>
  <link id="google-font-link" rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Open+Sans&display=swap">
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <div class="container">
    <h1>Avatar Studio</h1>

    <section class="controls">
      <div class="row">
        <label>Nom / seed avatar
          <input id="seedInput" placeholder="Ex : john123" />
        </label>
        <label>Style
          <select id="styleSelect">
            <option value="avataaars">avataaars</option>
            <option value="bottts">bottts</option>
            <option value="gridy">gridy</option>
            <option value="identicon">identicon</option>
          </select>
        </label>
        <button id="generateAvatarBtn">Générer l'avatar</button>
      </div>

      <div class="row">
        <label>Police (Google Fonts)
          <input id="fontInput" placeholder="Ex : Lora, Roboto, Montserrat" />
        </label>
        <button id="applyFontBtn">Appliquer police</button>
      </div>

      <div class="row">
        <label>Voix
          <select id="voicesSelect"></select>
        </label>
        <label>Vitesse
          <input id="rate" type="range" min="0.5" max="2" step="0.1" value="1" />
        </label>
      </div>

      <div class="row">
        <textarea id="speechText" rows="4" placeholder="Écris ici ce que l'avatar doit dire..."></textarea>
      </div>

      <div class="row">
        <button id="playBtn">▶️ Lire</button>
        <button id="stopBtn">⏹ Arrêter</button>
        <button id="downloadSrtBtn">Télécharger SRT</button>
        <button id="downloadAvatarBtn">Télécharger Avatar</button>
        <button id="recordVideoBtn">📹 Enregistrer vidéo (sans audio)</button>
      </div>
    </section>

    <section class="preview">
      <div id="avatarWrapper">
        <img id="avatarImg" alt="avatar" />
      </div>
      <canvas id="avatarCanvas" width="480" height="360"></canvas>
      <div id="subtitle" class="subtitle"></div>
    </section>

    <small>Note: Pour exporter une vidéo avec l'audio, regarde le README pour savoir comment intégrer un service TTS qui renvoie un fichier audio à combiner (ex: FFmpeg côté serveur).</small>
  </div>

  <script src="app.js"></script>
</body>
</html>
