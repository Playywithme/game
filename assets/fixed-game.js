(function () {
  "use strict";

  var config = window.GAME_CONFIG || {};
  var pieces = [];
  var selectedPiece = null;
  var placed = 0;
  var rows = 2;
  var cols = 2;
  var total = rows * cols;
  var els = {};

  function byId(id) {
    return document.getElementById(id);
  }

  function cacheEls() {
    [
      "introScreen", "gameScreen", "revealScreen", "board", "tray", "messageText",
      "progressText", "progressFill", "startButton", "againButton", "statusText",
      "confetti", "revealTitle", "finalArt"
    ].forEach(function (id) {
      els[id] = byId(id);
    });
  }

  function shuffle(items) {
    var copy = items.slice();
    for (var i = copy.length - 1; i > 0; i -= 1) {
      var j = Math.floor(Math.random() * (i + 1));
      var temp = copy[i];
      copy[i] = copy[j];
      copy[j] = temp;
    }
    return copy;
  }

  function pieceStyle(index) {
    var col = index % cols;
    var row = Math.floor(index / cols);
    return {
      x: (col * 100) + "%",
      y: (row * 100) + "%"
    };
  }

  function makePiece(index) {
    var button = document.createElement("button");
    var pos = pieceStyle(index);
    button.type = "button";
    button.className = "piece";
    button.dataset.index = String(index);
    button.setAttribute("aria-label", "Puzzle piece " + (index + 1));
    button.style.backgroundPosition = pos.x + " " + pos.y;
    button.draggable = true;
    button.addEventListener("click", function () {
      selectPiece(button);
    });
    button.addEventListener("dragstart", function (event) {
      event.dataTransfer.setData("text/plain", String(index));
      selectPiece(button);
    });
    return button;
  }

  function makeSlot(index) {
    var slot = document.createElement("button");
    slot.type = "button";
    slot.className = "slot";
    slot.dataset.index = String(index);
    slot.setAttribute("aria-label", "Puzzle place " + (index + 1));
    slot.addEventListener("click", function () {
      if (selectedPiece) {
        tryPlace(selectedPiece, slot);
      }
    });
    slot.addEventListener("dragover", function (event) {
      event.preventDefault();
      slot.classList.add("is-hover");
    });
    slot.addEventListener("dragleave", function () {
      slot.classList.remove("is-hover");
    });
    slot.addEventListener("drop", function (event) {
      event.preventDefault();
      slot.classList.remove("is-hover");
      var index = event.dataTransfer.getData("text/plain");
      var piece = els.tray.querySelector('.piece[data-index="' + index + '"]');
      if (piece) {
        tryPlace(piece, slot);
      }
    });
    return slot;
  }

  function selectPiece(piece) {
    if (piece.classList.contains("is-locked")) {
      return;
    }
    if (selectedPiece) {
      selectedPiece.classList.remove("is-selected");
    }
    selectedPiece = piece;
    selectedPiece.classList.add("is-selected");
    els.messageText.textContent = "Now tap where this piece belongs.";
  }

  function tryPlace(piece, slot) {
    if (slot.children.length) {
      els.messageText.textContent = "That spot is already filled.";
      return;
    }
    if (piece.dataset.index !== slot.dataset.index) {
      els.messageText.textContent = "Almost. Try another spot.";
      return;
    }
    piece.classList.remove("is-selected");
    piece.classList.add("is-locked");
    piece.draggable = false;
    slot.appendChild(piece);
    selectedPiece = null;
    placed += 1;
    updateProgress();
    els.messageText.textContent = "Nice. Keep going.";
    if (placed === total) {
      window.setTimeout(showReveal, 450);
    }
  }

  function updateProgress() {
    els.progressText.textContent = placed + " / " + total + " pieces placed";
    els.progressFill.style.width = ((placed / total) * 100) + "%";
  }

  function buildBoard() {
    els.board.innerHTML = "";
    els.tray.innerHTML = "";
    selectedPiece = null;
    placed = 0;
    pieces = [];
    for (var i = 0; i < total; i += 1) {
      els.board.appendChild(makeSlot(i));
      pieces.push(makePiece(i));
    }
    shuffle(pieces).forEach(function (piece) {
      els.tray.appendChild(piece);
    });
    updateProgress();
    els.messageText.textContent = "Tap a piece, then tap its matching place.";
  }

  function showIntro() {
    els.introScreen.classList.remove("hidden");
    els.gameScreen.classList.remove("is-active");
    els.revealScreen.classList.remove("is-active");
    els.statusText.textContent = "4 pieces";
  }

  function startGame() {
    buildBoard();
    els.introScreen.classList.add("hidden");
    els.gameScreen.classList.add("is-active");
    els.revealScreen.classList.remove("is-active");
    els.statusText.textContent = "Puzzle";
  }

  function showReveal() {
    els.gameScreen.classList.remove("is-active");
    els.revealTitle.textContent = config.REVEAL_MESSAGE;
    els.finalArt.innerHTML = '<img src="' + config.REVEAL_IMAGE + '" alt="">';
    els.revealScreen.classList.add("is-active");
    els.statusText.textContent = config.STATUS_LABEL;
    burstConfetti();
  }

  function burstConfetti() {
    var colors = config.CONFETTI_COLORS || ["#7eac7e", "#b58d42", "#5b9fe8", "#e9a3b6", "#ffffff"];
    els.confetti.innerHTML = "";
    for (var i = 0; i < 44; i += 1) {
      var bit = document.createElement("i");
      bit.style.left = (8 + Math.random() * 84) + "%";
      bit.style.bottom = (18 + Math.random() * 24) + "%";
      bit.style.background = colors[i % colors.length];
      bit.style.animationDelay = (Math.random() * 280) + "ms";
      els.confetti.appendChild(bit);
    }
    window.setTimeout(function () {
      els.confetti.innerHTML = "";
    }, 1800);
  }

  function init() {
    document.body.classList.remove("no-js");
    document.body.classList.add("js");
    document.body.dataset.variant = config.VARIANT;
    cacheEls();
    document.documentElement.style.setProperty("--accent", config.ACCENT || "#7eac7e");
    document.documentElement.style.setProperty("--puzzle-image", "url('" + config.PUZZLE_IMAGE + "')");
    els.startButton.addEventListener("click", startGame);
    els.againButton.addEventListener("click", startGame);
    showIntro();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
