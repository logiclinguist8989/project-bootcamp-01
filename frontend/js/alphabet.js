document.addEventListener('DOMContentLoaded', () => {
  const playBtn = document.querySelector('.btn--play');
  const modal = document.getElementById('alphabetModal');
  const backdrop = document.getElementById('alphabetBackdrop');
  const homeBtn = document.getElementById('alphabetHome');
  const cardsContainer = document.getElementById('alphabetCards');
  const targetEl = document.getElementById('targetLetter');
  const hearBtn = document.getElementById('hearAgain');
  const doneBtn = document.getElementById('doneAlphabet');
  const pauseBtn = document.getElementById('alphabetPause');
  const progressFill = document.getElementById('alphabetProgressFill');
  const levelText = document.getElementById('alphabetLevelText');
  const scoreText = document.getElementById('alphabetScore');
  const hintText = document.getElementById('hintText');

  let letters = [];
  let target = null;
  let currentScore = 0;
  let totalQuestions = 5;
  let currentQuestion = 0;
  let level = 1;

  // Word associations for each letter
  const letterWords = {
    'A': 'Apple', 'B': 'Banana', 'C': 'Cat', 'D': 'Dog', 'E': 'Elephant',
    'F': 'Fish', 'G': 'Giraffe', 'H': 'House', 'I': 'Ice', 'J': 'Juice',
    'K': 'Kite', 'L': 'Lion', 'M': 'Moon', 'N': 'Nest', 'O': 'Orange',
    'P': 'Pig', 'Q': 'Queen', 'R': 'Rabbit', 'S': 'Sun', 'T': 'Tree',
    'U': 'Umbrella', 'V': 'Violin', 'W': 'Water', 'X': 'X-Ray', 'Y': 'Yacht', 'Z': 'Zebra'
  };

  // Hints for each letter (characteristic features)
  const letterHints = {
    'A': 'Look for the pointy top! Like a mountain!',
    'B': 'Two bumps on the right side!',
    'C': 'It\'s like a crescent moon!',
    'D': 'A straight line with a big curve!',
    'E': 'Three lines across!',
    'F': 'Two lines across at the top!',
    'G': 'A circle with a line inside!',
    'H': 'Two tall lines with a bridge!',
    'I': 'A tall straight line!',
    'J': 'A line with a hook at the bottom!',
    'K': 'Two lines meeting in the middle!',
    'L': 'One tall line, one short at the bottom!',
    'M': 'Two mountains together!',
    'N': 'Two lines with a diagonal bridge!',
    'O': 'A perfect circle!',
    'P': 'A line with a bump at the top!',
    'Q': 'A circle with a tail!',
    'R': 'Like a P with a leg!',
    'S': 'A wiggly snake shape!',
    'T': 'One line across the top!',
    'U': 'A horseshoe shape!',
    'V': 'Two lines meeting at the bottom!',
    'W': 'Two V\'s together!',
    'X': 'Two lines crossing!',
    'Y': 'A line splitting into two!',
    'Z': 'Three lines making a zigzag!'
  };

  function showModal(){
    modal.setAttribute('aria-hidden','false');
    currentScore = 0;
    currentQuestion = 0;
    level = 1;
    loadLetters();
  }

  function hideModal(){
    modal.setAttribute('aria-hidden','true');
  }

  playBtn?.addEventListener('click', showModal);
  homeBtn?.addEventListener('click', hideModal);
  backdrop?.addEventListener('click', hideModal);
  doneBtn?.addEventListener('click', hideModal);
  pauseBtn?.addEventListener('click', () => {
    // TODO: Implement pause functionality
    showToast('Game paused');
  });

  async function loadLetters(){
    try{
      const apiBase = window.API_BASE_URL || '';
      const res = await fetch(`${apiBase}/api/letters`);
      const data = await res.json();
      letters = data.letters || [];
      pickTarget();
      updateProgressUI();
    }catch(err){
      console.error('letters fetch failed', err);
    }
  }

  function pickTarget(){
    // Pick a random letter as target
    const availableLetters = letters.filter(l => !l.completed);
    const lettersToChooseFrom = availableLetters.length > 0 ? availableLetters : letters;
    const randomLetter = lettersToChooseFrom[Math.floor(Math.random() * lettersToChooseFrom.length)];
    target = randomLetter.letter;
    
    // Pick 2 other random letters (different from target)
    const otherLetters = letters.filter(l => l.letter !== target);
    const shuffled = otherLetters.sort(() => Math.random() - 0.5);
    const options = [target, shuffled[0]?.letter, shuffled[1]?.letter].filter(Boolean);
    
    // Shuffle the options so target is in random position
    const shuffledOptions = options.sort(() => Math.random() - 0.5);
    
    renderCards(shuffledOptions);
    targetEl.textContent = target;
    targetEl.className = 'target-highlight';
    
    // Update hint
    if (hintText) {
      hintText.textContent = letterHints[target] || 'Can you find it?';
    }
    
    // Play audio for target letter
    playLetterAudio(target);
    currentQuestion++;
    updateQuestionUI();
  }

  function renderCards(letterOptions){
    cardsContainer.innerHTML = '';
    
    letterOptions.forEach(letter => {
      const isCorrect = letter === target;
      const card = document.createElement('div');
      card.className = `alphabet-card ${isCorrect ? 'correct' : ''}`;
      card.setAttribute('data-letter', letter);

      // Speaker icon
      const speakerIcon = document.createElement('button');
      speakerIcon.className = 'card-speaker';
      speakerIcon.setAttribute('aria-label', `Play sound for ${letter}`);
      speakerIcon.innerHTML = '🔊';
      speakerIcon.addEventListener('click', (e) => {
        e.stopPropagation();
        playLetterAudio(letter);
      });

      // Letter display
      const letterEl = document.createElement('div');
      letterEl.className = 'card-letter';
      letterEl.textContent = letter;

      // Word display (only for correct answer)
      let wordEl = null;
      if (isCorrect) {
        wordEl = document.createElement('div');
        wordEl.className = 'card-word';
        wordEl.textContent = letterWords[letter] || '';
      }

      card.appendChild(speakerIcon);
      card.appendChild(letterEl);
      if (wordEl) card.appendChild(wordEl);

      card.addEventListener('click', () => onCardClick(letter, card));

      cardsContainer.appendChild(card);
    });
  }

  hearBtn?.addEventListener('click', () => {
    if (target) {
      playLetterAudio(target);
    }
  });

  async function onCardClick(letter, cardEl){
    const clicked = letter;
    const correct = clicked === target;

    // Play audio for clicked letter
    playLetterAudio(clicked);

    if (correct){
      cardEl.classList.add('selected');
      cardEl.classList.remove('incorrect');
      
      // Update score
      currentScore++;
      
      // Inform server of successful progress
      const apiBase = window.API_BASE_URL || '';
      const res = await fetch(`${apiBase}/api/progress`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ letter: clicked, correct: true })
      });
      const data = await res.json();
      
      // Update UI
      updateProgressUI();
      showToast(`Great! You found ${clicked} — +${data.granted.stars || 0} stars`);
      
      // Check if we've completed enough questions
      if (currentQuestion >= totalQuestions) {
        setTimeout(() => {
          showToast(`Level ${level} complete! Score: ${currentScore}/${totalQuestions}`);
          level++;
          currentQuestion = 0;
          currentScore = 0;
          pickTarget();
        }, 1000);
      } else {
        // Pick a new target after a delay
        setTimeout(() => { pickTarget(); }, 1000);
      }
    } else {
      // Show incorrect feedback
      cardEl.classList.add('incorrect');
      setTimeout(() => cardEl.classList.remove('incorrect'), 700);
      
      // Inform server of attempt
      const apiBase = window.API_BASE_URL || '';
      await fetch(`${apiBase}/api/progress`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ letter: clicked, correct: false })
      });
      showToast('Try again!');
    }
  }

  function playLetterAudio(letter){
    // Play the pronunciation sound for the letter (e.g., "A" pronounced as "ay")
    // Audio files should be named: A.mp3, B.mp3, etc. in frontend/assets/audio/
    const url = `/assets/audio/${letter}.mp3`;
    const audio = new Audio(url);
    
    // Try to play the pronunciation audio file
    audio.play().catch(err => {
      console.warn(`Could not play audio for letter ${letter}:`, err);
      // Fallback to a beep tone if audio file is missing
      beepTone(880, 0.12);
    });
  }

  function beepTone(freq, duration){
    try{
      const ctx = new (window.AudioContext || window.webkitAudioContext)();
      const o = ctx.createOscillator();
      const g = ctx.createGain();
      o.type = 'sine';
      o.frequency.value = freq;
      o.connect(g);
      g.connect(ctx.destination);
      g.gain.setValueAtTime(0.0001, ctx.currentTime);
      g.gain.exponentialRampToValueAtTime(0.2, ctx.currentTime + 0.01);
      o.start();
      setTimeout(() => { o.stop(); ctx.close(); }, duration * 1000);
    }catch(e){
      console.warn('beep failed', e);
    }
  }

  function updateQuestionUI(){
    // Update level text
    if (levelText) {
      levelText.textContent = `Level ${level}`;
    }
    
    // Update score
    if (scoreText) {
      scoreText.textContent = `${currentScore}/${totalQuestions}`;
    }
    
    // Update progress bar (based on current question)
    const progressPercent = (currentQuestion / totalQuestions) * 100;
    if (progressFill) {
      progressFill.style.width = progressPercent + '%';
    }
  }

  async function updateProgressUI(){
    // Compute completed letters
    const apiBase = window.API_BASE_URL || '';
    try {
      const res = await fetch(`${apiBase}/api/letters`);
      const data = await res.json();
      letters = data.letters || letters;
      
      // Update stars count
      const r = await fetch(`${apiBase}/api/rewards`);
      const rewards = await r.json();
      const stars = document.getElementById('starsCount');
      if (stars) stars.textContent = rewards.stars ?? stars.textContent;
    } catch(err) {
      console.error('Failed to update progress UI', err);
    }
  }

  function showToast(msg){
    const toast = document.getElementById('toast');
    if (toast) {
      toast.textContent = msg;
      toast.style.display = 'block';
      setTimeout(() => { toast.style.display = 'none'; }, 1600);
    }
  }
});
